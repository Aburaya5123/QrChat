### ローカル実行

```
./run-local.sh --rootpw [MYSQL_ROOT_PASSWORD] --userpw [MYSQL_USER_PASSWORD] --djangosr [SECRET_KEY(django)]
```
もしくは、```/local_container``` 配下で以下のコマンドを実行 ```docker compose up --build```。  
事前に```/local_container/secret_keys``` 配下にKEYを格納したテキストファイルを用意する。  
テキストファイル作成後は、```chmod 0444``` で読み取り専用にする。  
#### PORT  
django :8000  
flower(Celeryのモニター) :5555  
<br>
### リモート実行 (GCPにデプロイ)
手順
1. 事前準備としてGCPにプロジェクトを作成し、課金の請求先を設定する。
2. ```/deployment-settings.tfvars``` にプロジェクトIDやリージョンを含めた情報を入力。
3. 任意: ```/dev-env``` 配下で作成したコンテナに入る。(Cloud shellで実行する場合は不要、たぶん)
4. 以下のコマンドでプロジェクトにログイン  
  ```gcloud init && gcloud auth application-default login && gcloud auth application-default set-quota-project ${YOUR_PROJECT_ID}```
5. ```./run-remote.sh```を実行
6. デプロイ完了まで20分程度
7. SecretManagerに格納されている 'STATIC_IP' を自身のドメインのaレコードに設定
8. ```kubectl describe managedcertificate managed-cert```で、StatusがActiveになっていれば設定したドメインからHTTPSでアクセスできる。
<br>
注意点として、kubectlでのオブジェクト作成は以下の順序で行う。

External secret -><br>
(frontend-conf, backend-conf, managed-cert) -><br>
deployment.yaml -><br>
service.yaml -><br>
managed-cert-ingress.yaml<br>   
最後の3つが厄介で、deploymentが後から作成されるとHealthCheckのパスが正しく設定されずにエラーが出る。  
Unhealty...というエラーがでたら、最後の3つを消して再度applyする。  
<br>
また、今回はとりあえずデプロイすることが目的だったので、yamlの中の変数はenvsubstで無理やり押し込んでいる。  
なので、個別に実行する場合は環境変数を渡す必要がある。  
helmをつかえばもっと上手くできるみたい。  
<br>
インフラに関しても、とりあえず必要なものは全部詰め込んだので、放っておくとお財布が大変なことになる。  
もっと効率よくできるように勉強しないと。  
<br>




<img src="https://github.com/Aburaya5123/QrChat/assets/166899082/5a98f5f2-d5f6-4b7f-8465-dfedc96a933e" width=600>  
<br>
<img src="https://github.com/Aburaya5123/QrChat/assets/166899082/bc1a14b0-b23d-43d6-a2c3-dbb9f8362d64" width=600>  
<br>
<img src="https://github.com/Aburaya5123/QrChat/assets/166899082/17dacacc-5e15-4a36-a29f-af984de89b96" width=600>  
<br>
<img src="https://github.com/Aburaya5123/QrChat/assets/166899082/4bb6417e-d881-4a83-8f5c-479eb79fdaca" height=400>  
