### ローカル実行
※06/12 秘密鍵の保管場所を移動させたため、初回起動時に限りrun.shの実行が必要
```
./run.sh --rootpw MYSQL_ROOT_PASSWORD --userpw MYSQL_USER_PASSWORD --djangosr SECRET_KEY(settings.py)
```
手動で秘密鍵ファイルの追加を行う場合は、/secret_keys 配下にKEYを格納したテキストファイルを作成し、chmod 0444 で読み取り専用とする。


### PORT  
django :8000  
flower(Celeryのモニター) :5555  
<br>

<img src="https://github.com/Aburaya5123/QrChat/assets/166899082/5a98f5f2-d5f6-4b7f-8465-dfedc96a933e" width=600>  
<br>
<img src="https://github.com/Aburaya5123/QrChat/assets/166899082/bc1a14b0-b23d-43d6-a2c3-dbb9f8362d64" width=600>  
<br>
<img src="https://github.com/Aburaya5123/QrChat/assets/166899082/17dacacc-5e15-4a36-a29f-af984de89b96" width=600>  
<br>
<img src="https://github.com/Aburaya5123/QrChat/assets/166899082/4bb6417e-d881-4a83-8f5c-479eb79fdaca" height=400>  
