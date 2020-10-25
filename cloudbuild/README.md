# 概要
CloudBuildの処理を設定するディレクトリ。

# 準備
## トリガーの作成
- airflowとfunctions用にそれぞれCloudBuildのトリガーを作成。
- aiflowのトリガーには`_USER_INSTANCE` `_ZONE`変数を設定。
    - `_USER_INSTANCE`は`username@instancename`など
    - `_ZONE`は`us-west1-a`など

## 権限の設定
CloudBuild管理画面の設定から以下を有効化（いずれも必須）。

- CloudFunctions（CloudFunctions開発者）
- ComputeEngine（Computeインスタンス管理者）
- ServiceAccounts（サービスアカウントユーザー）

## その他
- [Resource Manager API](https://cloud.google.com/resource-manager/docs/apis?hl=ja)を有効化
    - CloudFunctionsに一つしか関数がない状態では必要なかったが、二つ目から何故か要求された。

# 注意
- 初回のみ未認証の関数呼び出しの許可を行う。
    - CloudFunctionsの管理画面から各関数にとび、allUsersにcloudfunctions.invokerロールを付与。
    - `--ingress-settings internal-only`の制限があるから問題ないはず。
