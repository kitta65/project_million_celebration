# 100万再生お祝いbot

## 概要
YouTubeのAPI経由で動画の再生回数を取得し、100万再生達成を検知したら自動でお祝いするbot。
あくまで自分のためのbotなので、誰かに使ってもらうための`README.md`にはなっていない。


## 設定
`./functions/channel_list.py`がYouTubeの検索条件を決めるファイル。書き換えたら`./functions/deploy.sh`を実行して反映すること。

```
# channels
channels = [
    {
        "name": "子兎音様",
        "playlists": ["PL4PDyA42kQIz6SLG-2AuVP79xEpFGLoun", "PL4PDyA42kQIxNss1PEt99u76zQtemIgAO"],
        "tag": "#ことね教"
    },
    {
        "name": "アイちゃん",
        "playlists": ["PL0bHKk6wuUGIAmzzqdVMynRrAOi8odYFQ", "PL0bHKk6wuUGLWGipKSf0dFrpuzDitERqD"],
        "tag": "#KizunaAI #KizunaAIMusic"
    }
]
```

### name
Twitterで投稿する際の表記。敬称も忘れずに。

### playlists
再生リストのURLに`list=xxx`の形式で含まれるもの。複数指定する場合、重複があっても問題ない。

### tag
Twitterで投稿する際のハッシュタグ。複数付ける場合は半角スペースで区切る。


