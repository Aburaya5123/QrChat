from django.shortcuts import redirect
from django.contrib.auth import logout
from logging import getLogger
from django.contrib import messages

from qrchat.utils.model_helper import find_room_object, str_to_uuid


logger = getLogger(__name__)


class PathPattern:
    # url一覧
    path_pattern = {'root':'/', 
                    'accounts':'/accounts/', 
                    'chat':'/chat/', 
                    'admin':'/admin/', 
                    'admin_login':'/accounts/authlogin/',
                    'login':'/accounts/login/', 
                    'logout':'/accounts/logout/', 
                    'signup':'/accounts/signup/',
                    'room-settings':'/accounts/room-settings/', 
                    'chatroom':'/chat/room/', 
                    'lobby':'/chat/lobby/',
                    'favicon':'/favicon.ico/',
                    'media':'/media/',
                    'healthz':'/healthz' }


class AccessControlMiddleware:

    def process_response(self, request, response):
        response['Cache-Control'] = 'no-store, no-cache'
        return response

    def __init__(self, get_response):
        self.get_response = get_response
        self.path_pattern = PathPattern.path_pattern

    def __call__(self, request):

        # ヘルスチェック
        if request.path.startswith(self.path_pattern['healthz']):
            return self.get_response(request)

        destination = request.path
        destinations = destination.strip('/').split('/')
        self.is_authenticated = request.user.is_authenticated
        self.is_guest = request.user.is_guest if self.is_authenticated else None
        self.username = request.user.username if self.is_authenticated else None
        self.joined_room = request.user.joined_room if self.is_authenticated else None

        #print(f"【MiddleWare】Auth:{self.is_authenticated}/U_ID:{request.user}/PATH:{request.path}")

        if not destination.endswith('/'):
            destination += '/'
            request.path += '/'

        # 管理画面
        if destination.startswith(self.path_pattern['admin']):
            return self.get_response(request)
        
        # アイコン取得
        elif destination.startswith(self.path_pattern['favicon']):
            return redirect('/static/icons/favicon.ico')
        
        # メディアへのアクセス
        elif destination.startswith(self.path_pattern['media']):
            return self.get_response(request)

        # ログイン画面
        elif destination.startswith(self.path_pattern['login']):
            return self.login_access_control(request, destinations)

        # ログアウト画面
        elif destination.startswith(self.path_pattern['logout']):
            return self.logout_access_control(request, destinations)
           
        # 新規登録画面
        elif destination.startswith(self.path_pattern['signup']):
            return self.signup_access_control(request, destinations)
        
        # ルーム名設定画面
        elif destination.startswith(self.path_pattern['room-settings']):
            return self.room_settings_access_control(request, destinations)

        # ロビー画面
        elif destination.startswith(self.path_pattern['lobby']):
            return self.lobby_access_control(request, destinations)

        # チャットルーム画面
        elif destination.startswith(self.path_pattern['chatroom']):
            return self.chat_room_access_control(request, destinations)

        else:
            return redirect(self.path_pattern['login']) 


    def login_access_control(self, request, destinations):
        if self.is_authenticated:
            # ゲストはログアウト後に、ログイン画面へ遷移
            if self.is_guest:
                return redirect(self.path_pattern['logout'])
            # ログイン済みのユーザーは、ルーム名設定画面へ遷移
            else:
                return redirect(self.path_pattern['room-settings'])
        else:
            return self.get_response(request)
    

    def logout_access_control(self, request, destinations):
        if self.is_authenticated:
            return self.get_response(request)
        else:
            return redirect(self.path_pattern['login'])
        

    def signup_access_control(self, request, destinations):
        if self.is_authenticated:
            # ゲストは、ログアウト後に遷移
            if self.is_guest:
                logout(request)
                return self.get_response(request)
            # ログイン済みの場合はルーム名設定画面に遷移
            else:
                return redirect(self.path_pattern['room-settings'])
        else:
            return self.get_response(request)
        
    
    def room_settings_access_control(self, request, destinations):
        if self.is_authenticated:
            # ゲストはこの画面へアクセスできないので、ロビーへリダイレクト
            if self.is_guest and find_room_object(False, room_id=self.joined_room):
                return redirect(self.path_pattern['lobby'] + str(self.joined_room) + '/')
            # 部屋が見つからない場合
            elif self.is_guest:
                messages.error(request, 'ルームが見つかりません。')
                return redirect(self.path_pattern['logout'])
            else:
                return self.get_response(request)        
        else:
            return redirect(self.path_pattern['login'])
        

    def lobby_access_control(self, request, destinations):
        if self.is_authenticated:
            # ルームIDの指定なし
            if len(destinations) == 2:
                # 参加済みのルームがあればルームIDを追加してリダイレクト
                if find_room_object(False, room_id=self.joined_room):
                    return redirect(self.path_pattern['lobby'] + str(self.joined_room) + '/')
                # ゲストユーザーは1つのルームに紐づけられているので、joined_roomが見つからない場合はログアウト
                elif self.is_guest:
                    messages.error(request, 'ルームが見つかりません。')
                    return redirect(self.path_pattern['logout'])
                messages.error(request, 'ルームが見つかりません。')
                return redirect(self.path_pattern['login'])
            else:
                room_instance = find_room_object(True, room_id=str_to_uuid(destinations[2]))
                if room_instance is not None:
                    # 既に参加しているルームとアクセス先のルームが異なる場合はログアウト後に遷移
                    if self.joined_room != room_instance.first().room_id:
                        logout(request)
                    return self.get_response(request)
                else:
                    messages.error(request, 'ルームが見つかりません。')
                    if self.is_guest:
                        return redirect(self.path_pattern['logout'])
                    else:
                        return redirect(self.path_pattern['login'])
        else:
            # ルームIDの指定なし
            if len(destinations) == 2:
                return redirect(self.path_pattern['login'])
            else:
                if find_room_object(False, room_id=str_to_uuid(destinations[2])):                
                    return self.get_response(request)
                else:
                    messages.error(request, 'ルームが見つかりません。')
                    return redirect(self.path_pattern['login'])


    def chat_room_access_control(self, request, destinations):
        if self.is_authenticated:
            if len(destinations) == 2:
                # 参加済みのルームがあり、ニックネームが設定されていればルームIDを追加してリダイレクト
                if find_room_object(False, room_id=self.joined_room) and self.username is not None:
                    return redirect(self.path_pattern['chatroom'] + str(self.joined_room) + '/')
                # ユーザー名の設定がない場合は、ロビーへリダイレクト
                elif find_room_object(False, room_id=self.joined_room):
                    return redirect(self.path_pattern['lobby'] + str(self.joined_room) + '/')
                # ゲストユーザーは1つのルームに紐づけされているので、joined_roomが見つからない場合は削除
                elif self.is_guest:
                    return redirect(self.path_pattern['logout'])
                return redirect(self.path_pattern['login'])
            else:
                room_instance = find_room_object(True, room_id=str_to_uuid(destinations[2]))
                if room_instance is not None:
                    # joined_roomとurlが一致、かつユーザー名が設定されている場合にのみアクセス許可
                    if self.joined_room == room_instance.first().room_id and self.username:
                        return self.get_response(request)
                    return redirect(self.path_pattern['lobby'] + str(room_instance.first().room_id) + '/')
                else:
                    messages.error(request, 'ルームが見つかりません。')
                    if self.is_guest:
                        return redirect(self.path_pattern['logout'])
                    else:
                        return redirect(self.path_pattern['login'])
        else:
            if len(destinations) == 2:
                return redirect(self.path_pattern['login'])
            else:
                room_instance = find_room_object(True, room_id=str_to_uuid(destinations[2]))
                if room_instance is not None:                
                    return redirect(self.path_pattern['lobby'] + str(room_instance.first().room_id) + '/')
                else:
                    messages.error(request, 'ルームが見つかりません。')
                    return redirect(self.path_pattern['login'])