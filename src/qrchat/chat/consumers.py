import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from typing import NoReturn
from uuid import UUID
from django.utils import timezone
from datetime import datetime
from channels.exceptions import StopConsumer

from qrchat.utils.model_helper import get_historical_chat_messages, create_room_messages, channel_consumer_update


class ChatConsumer(AsyncWebsocketConsumer):

    async def websocket_connect(self, message) -> None|NoReturn:
        self.user = self.scope['user']

        if self.user.is_authenticated and type(self.user.joined_room) is UUID:
            await self.channel_layer.group_add(
                str(self.user.joined_room),
                self.channel_name )
            await self.accept()
            # 履歴の送信
            await self.on_first_connected()
            # 参加人数の更
            await self.update_online_counter(True)
        else:
            self.close()
            raise StopConsumer()

    async def websocket_disconnect(self , close_code) -> NoReturn:
        self.user = self.scope['user']
        #print(f"USER: {self.user} has Disconnected.")

        if self.user.is_authenticated and type(self.user.joined_room) is UUID:
            # 参加人数の更新
            await self.update_online_counter(False)
            await self.channel_layer.group_discard(
                str(self.user.joined_room), 
                self.channel_name )
        await self.close()
        raise StopConsumer()

    async def receive(self, text_data) -> None:
        self.user = self.scope['user']

        if self.user.is_authenticated and type(self.user.joined_room) is UUID:
            text_data_json = json.loads(text_data)

            try:
                message = text_data_json["message"]
                if message == "":
                    return

                time_stamp = timezone.now()
                # ChatMessageの作成
                await self.create_chat_object(
                    self.user.username,
                    self.user.joined_room,
                    self.user.user_icon,
                    message, 
                    time_stamp)
                await self.channel_layer.group_send(
                    str(self.user.joined_room),{
                        "type" : "chat_message",
                        "message_type": "chat",
                        "message" : message,
                        "username" : self.user.username,
                        "created_at": str(time_stamp),
                        "icon": self.user.user_icon
                    })
            except Exception:
                # ルーム削除後に遅れてメッセージが送信された際にキャッチ
                pass

    async def chat_message(self , event) -> None: 
        message = event["message"]
        username = event["username"]
        created_at = event["created_at"]
        icon = event["icon"]
        await self.send(text_data = json.dumps({"content":message ,
                                                "name":username, 
                                                "created_at":str(created_at),
                                                "icon":icon},
                                                ensure_ascii=False))

    # ルーム参加人数の通知
    async def member_counter(self, event) -> None:
        counter = event["counter"]
        await self.send(text_data = json.dumps({
                "message": counter, 
                "message_type":"counter"},
                ensure_ascii=False))
    
    # システム通知
    async def system_notification(self, event) -> None|NoReturn:
        code = event["code"] # HTTPステータスコード
        await self.send(text_data = json.dumps({
                "message":code, 
                "message_type":"system"},
                ensure_ascii=False))
        if code == 410:
            await self.channel_layer.group_discard(
                str(self.user.joined_room),
                self.channel_name)
            await self.close()
            raise StopConsumer()
        
    # 指定ユーザーをWebsocketから切断
    async def disconnect_user(self, event) -> NoReturn:
        self.user = self.scope['user']
        if event['user_id'] == str(self.user.user_id):
            code = event['code']
            if code == 419:
                await self.send(text_data = json.dumps({
                    "message":code, 
                    "message_type":"system"},
                    ensure_ascii=False))
            await self.channel_layer.group_discard(
                str(self.user.joined_room),
                self.channel_name)
            await self.close()
            raise StopConsumer()

    # ChatMessageオブジェクト作成
    @database_sync_to_async
    def create_chat_object(self, name:str, joined_room:UUID, user_icon:str, message:str, created_at:datetime) -> None:
        create_room_messages(name, 
                             message, 
                             created_at, 
                             joined_room,
                             user_icon)

    # チャット履歴の送信
    async def on_first_connected(self) -> None:
        historical_data = await self.get_historical_data()
        if historical_data is not None:
            await self.send(text_data = json.dumps({
                "message": historical_data, 
                "message_type":"history", 
                "username":self.user.username},
                ensure_ascii=False))

    # チャット履歴の取得
    @database_sync_to_async
    def get_historical_data(self) -> dict|None:
        return get_historical_chat_messages(self.user.joined_room)
    
    # 参加人数の更新
    async def update_online_counter(self, connected) -> None:
        counter = await self.update_channel_consumer(connected)
        await self.channel_layer.group_send(
                str(self.user.joined_room),{
                    "type" : "member_counter",
                    "counter": counter
                })
    
    # 参加人数の更新(同期)
    @database_sync_to_async
    def update_channel_consumer(self, connected) -> int:
        return channel_consumer_update(connected, 
                                       self.user.joined_room, 
                                       self.user)