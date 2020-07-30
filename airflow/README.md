# 前提
- `airflow shceduler`が起動している。
- `airflow.cfg`で`dags_are_paused_at_creation = False`を設定している。

# 導入
## configの作成
`./dags/million_celebration_pkg`以下に`million_celebration_config.py`を作成。内容は以下。

```
sandbox_token = "xxxxx"
gcp_project = "xxxxx"
```

## dagの登録
`./dags`に移動して以下を実行。環境変数`AIRFLOW_HOME`をいじっている場合、パスを修正する必要があるかもしれない。

```
zip -r $HOME/airflow/dags/morning_ai_bot *
```

