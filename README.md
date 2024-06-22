### 概要  

Djangoで開発したWEBチャットアプリ。  
誰でも匿名で参加できるチャットサービス。  
https://www.qrchat.aburaya5123.com/  
<br>
ログイン画面でアカウントを新規作成するとチャットルームを開くことができ、同時にチャットルームのオーナーとなる。  
ルーム作成時に一意なURLとQRコードが発行され、これらを知る者のみチャットに参加可能となる。  
オーナーと違い参加者はアカウント作成を行う必要はなく、ニックネームだけを設定すれば匿名で参加できる。  
なので、不特定多数が集まる場で匿名で意見交換を行うツールとしての利用を想定している。  
<br>
### 構成  
フレームワーク: Django  
データベース: MySQL (CloudSQL)  
キャッシュ: Redis (Memorystore)  
ストレージ: Cloud Storage  
タスク実行: Celery  
コンテナ実行: Kubernetes (docker compose)  
Iac: Terraform  
<br>

### リモート実行 (GCPにデプロイ)
手順
1. 事前準備としてGCPにプロジェクトを作成し、課金の請求先を設定する。
2. ```/deployment-settings.tfvars``` にプロジェクトIDやリージョンを含めた情報を入力。
3. ```/dev-env``` 配下で作成したコンテナに入る。(Cloud shellで実行する場合は不要、たぶん)
4. ```./run-remote.sh```を実行。
5. デプロイ完了まで20分程度。
6. ```kubectl get ingress``` コマンドで表示される 'managed-cert-ingress' のaddressを自身のドメインのaレコードに設定。
7. ```kubectl describe managedcertificate managed-cert```のStatusがActiveかつ、dnsの設定が完了していればHTTPSでアクセス可能となる。
8. 追記 06/22: Loadbalancerの外部IPへの直接アクセス, 国外からのアクセスをブロックするポリシーをCloudArmorで追加。
<br>
注意点として、kubectlでのオブジェクト作成は以下の順序で行う。

(External secret ->)<br>
frontend-conf, backend-conf, managed-cert -><br>
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





<img src="https://github.com/Aburaya5123/QrChat/assets/166899082/5a98f5f2-d5f6-4b7f-8465-dfedc96a933e" width=600>  
<br>
<img src="https://github.com/Aburaya5123/QrChat/assets/166899082/bc1a14b0-b23d-43d6-a2c3-dbb9f8362d64" width=600>  
<br>
<img src="https://github.com/Aburaya5123/QrChat/assets/166899082/17dacacc-5e15-4a36-a29f-af984de89b96" width=600>  
<br>
<img src="https://github.com/Aburaya5123/QrChat/assets/166899082/4bb6417e-d881-4a83-8f5c-479eb79fdaca" height=400>  
