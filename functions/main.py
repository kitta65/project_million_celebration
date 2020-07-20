from googleapiclient.discovery import build
import config
import pandas as pd
import datetime
from google.cloud import bigquery
from twitter import Twitter, OAuth
import time
import numpy as np
import channel_list

# create latest table
def fetch_info_in_playlist(client, playlist_id, next_page_token=None):
    # call YouTube playlistItems API
    arg = {
        "playlistId": playlist_id,
        "part": "snippet",
        "maxResults": 50
    }
    if next_page_token is not None: arg["pageToken"] = next_page_token
    response_playlist_item = client.playlistItems().list(**arg).execute()
    video_ids = [x["snippet"]["resourceId"]["videoId"] for x in response_playlist_item["items"]]
    # call YouTube videos API
    response_videos = client.videos().list(
        id=",".join(video_ids),
        part="statistics",
        maxResults=50
    ).execute()
    view_counts = [
        int(x["statistics"].get("viewCount", "-1")) for x in response_videos["items"]
    ] # -1... videos limitted for membership
    result = pd.DataFrame({
        "playlist_id": playlist_id,
        "video_id": video_ids,
        "view_count": view_counts
    }).query("view_count >= 0")
    # exec recursively
    next_page_token = response_playlist_item.get("nextPageToken", None)
    if next_page_token is None:
        return result
    else:
        result = pd.concat([
            result,
            fetch_info_in_playlist(
                client=client,
                playlist_id=playlist_id,
                next_page_token=next_page_token
            )
        ], ignore_index=True)
        return result

def main_upload(requests):
    client_yt = build("youtube", "v3", developerKey=config.key, cache_discovery=False)
    client_bq = bigquery.Client(project=config.project_name)
    yyyymmdd = datetime.date.today().strftime('%Y%m%d')
    table = f"{config.project_name}.million_celebration.view_count_{yyyymmdd}"
    channels = channel_list.channels
    for c in channels:
        for p in c["playlists"]:
            df = fetch_info_in_playlist(client_yt, p)
            client_bq.load_table_from_dataframe(df, table)
            time.sleep(1)

# tweet celebrate message
def main_tweet(requests):
    client_bq = bigquery.Client(project=config.project_name)
    client_tw = Twitter(auth=OAuth(
        config.token,
        config.token_secret,
        config.consumer_key,
        config.consumer_secret
    ))
    yyyymmdd_today = datetime.date.today().strftime('%Y%m%d')
    yyyymmdd_yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y%m%d')
    table_today = f"{config.project_name}.million_celebration.view_count_{yyyymmdd_today}"
    table_yesterday = f"{config.project_name}.million_celebration.view_count_{yyyymmdd_yesterday}"
    query = f"""
        SELECT t.playlist_id, t.video_id
        FROM {table_today} as t inner join {table_yesterday} as y using(video_id)
        WHERE y.view_count < 1000000 and 1000000 <= t.view_count
    """
    query_job = client_bq.query(query)
    df = query_job.to_dataframe()
    channels = channel_list.channels
    for c in channels:
        df_each = df.query(f"playlist_id in {c['playlists']}")
        videos = np.unique(df_each["video_id"].values)
        if videos.shape[0] == 0: continue
        message_head = f"【自動】{c['name']}100万再生おめでとう！\n"
        message_body = "".join([f"https://www.youtube.com/watch?v={x}\n" for x in videos])
        message_tag = c["tag"]
        client_tw.statuses.update(status=message_head+message_body+message_tag)

