# 概要
Japan Vulnerability Notes (https://jvn.jp/)から脆弱性情報を取得し、指定したアドレスに通知メールを送るツールです。
定期実行環境を構築することにより、重大な脆弱性に関する情報収集を自動化し、見逃し防止になるかも！

# Docker-composeでの実行
```
docker-compose up -d
docker container exec -it my-python3 sh
```

```
docker container exec my-python3 python main.py
```

# TODO
- 通知先メールアドレスをGoogle Spread Sheetから取得しているが、他の手段でも指定できるようにする
- 特定のキーワードに関する脆弱性のみを取得できるようにする
- メール文をハードコードしているがテンプレート化する