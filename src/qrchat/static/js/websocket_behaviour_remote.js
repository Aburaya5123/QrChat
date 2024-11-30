$(document).ready(function () {

  // WebSocketコネクション
  const url = 'wss://www.qrchat.aburaya5123.com/ws/chat/';
  var ws = new WebSocket(url);

  // Templateからusernameの取得
  const username = unicodeToChar(document.getElementById('user-data').textContent.replace(/^"|"$/g, ''));

  ws.onopen = () => on_open();
  ws.onclose = () => on_close();

  // Chatを追加するHolder
  const messageHolder = document.querySelector('#chat-message-holder');

  // チャット送信ボタンが押された際のリスナー
  document.getElementById("send-chat-text").onclick = function sendMessage() {
    const input = document.getElementById('chat-text-area').value;

    if (input === "") {
      return
    }
    var sendData = {
      message: input,
    };
    ws.send(JSON.stringify(sendData));
    document.getElementById('chat-text-area').value = '';
  };

  function on_open() {
    updateOnlineStatus(true);
  }

  function on_close() {
    updateOnlineStatus(false);
  }
 
  // チャットオブジェクトの作成
  function createChatMessageElement(data) {
    // 画面下まで自動スクロールする場合はtrue
    var autoScroll = false

    // スクロールバーが下部に位置する場合は、自動スクロールを行う
    if (messageHolder.scrollHeight - (messageHolder.scrollTop + messageHolder.offsetHeight) <= 30){
      autoScroll = true;
    }

    // username === チャットの送信者 の場合は、チャットを画面右に表示させる(-> Templete2)
    if (data['name'].toString() === username) {
        template_num = 2;
    } else {
        template_num = 1;
    }

    // Templateからcloneを複製
    const chat_template = document.querySelector('#chat-template' + template_num.toString());
    const clone = document.importNode(chat_template.content, true);

    const date = new Date(data['created_at']);
    const formattedDate = `${(date.getMonth() + 1).toString().padStart(2, '0')}月${date.getDate().toString().padStart(2, '0')}日 ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}:${date.getSeconds().toString().padStart(2, '0')}`;

    clone.querySelector('#chat-message-sender' + template_num.toString()).textContent =  data['name'];
    clone.querySelector('#chat-message-body' + template_num.toString()).textContent = data['content'];
    clone.querySelector('#chat-message-date' + template_num.toString()).textContent = formattedDate;
    clone.querySelector('#chat-message-icon' + template_num.toString()).textContent = data['icon'];

    // アイコンが王冠の場合は、アイコンの背景色を変更
    if (data['icon'] === '♔' | data['icon'] === '♚') {
      clone.querySelector('#chat-message-icon-container' + template_num.toString()).style.backgroundColor = '#a0964c'
    }
    
    // Holderに追加
    messageHolder.appendChild(clone);

    if (autoScroll) {
      messageHolder.scrollTop = messageHolder.scrollHeight;
    }
  }

  // Unicodeを文字列に変換
  function unicodeToChar(text) {
    return text.replace(/\\u[\dA-F]{4}/gi, 
      function (match) {
          return String.fromCharCode(parseInt(match.replace(/\\u/g, ''), 16));
      });
 }

  // 参加人数の更新 
  function updateMemberCounter(counter) {
    const display = document.querySelector('#member-counter');
    display.textContent = "参加者 " + counter.toString() + "名";
  }

  // システム通知
  function systemMessageReceived(code) {
    switch (code) {
      case 410: // ルームが終了
        alert('このルームは終了しました。');
        document.getElementById("send-chat-text").style.display = 'none';
      case 419:
        alert('セッションの有効期限を過ぎたので、切断されました。');
        document.getElementById("send-chat-text").style.display = 'none';
    }
  }

  // オンラインステータスの更新
  function updateOnlineStatus(isOnline) {
    const statusElement = document.getElementById('online-status');
    const statusText = document.getElementById('status-text');
    if (isOnline) {
        statusElement.classList.add('online');
        statusElement.classList.remove('offline');
        statusText.textContent = 'ONLINE';
    } else {
        statusElement.classList.add('offline');
        statusElement.classList.remove('online');
        statusText.textContent = 'OFFLINE';
    }
}

  // Websocketメッセージ取得時のリスナー
  ws.onmessage = function (e) {
    const receiveData = JSON.parse(e.data);

    // チャット履歴の取得
    if (receiveData.message_type === 'history') {
      for (let i = 0; i < Object.keys(receiveData.message).length; i++) {
        createChatMessageElement(receiveData.message[i]);
        messageHolder.scrollTop = messageHolder.scrollHeight;
      }
    }
    // 参加人数の取得 
    else if (receiveData.message_type === 'counter') {
      updateMemberCounter(receiveData.message);
    }
    // システムメッセージの取得
    else if (receiveData.message_type === 'system') {
      systemMessageReceived(receiveData.message)
    }
    // チャットメッセージの取得
    else{
      createChatMessageElement(receiveData);
    }
  };
});