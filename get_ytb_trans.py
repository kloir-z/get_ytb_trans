from youtube_transcript_api import YouTubeTranscriptApi
from flask import jsonify
from urllib.parse import urlparse, parse_qs
from googleapiclient.discovery import build  # type: ignore
import os


def normalize_youtube_url(url):
    # 既存のコードは変更なし
    parsed_url = urlparse(url)
    if parsed_url.hostname in ("youtu.be", "m.youtube.com", "youtube.com", "www.youtube.com"):
        if parsed_url.hostname == "youtu.be":
            video_id = parsed_url.path.lstrip("/").split("?")[0]
        else:
            query = parse_qs(parsed_url.query)
            video_id = query.get("v", [None])[0]
        if video_id:
            return f"https://www.youtube.com/watch?v={video_id}", video_id
    return url, None


def get_ytb_trans(request):
    try:
        url = request.args.get("url")
        print(f"Received URL: {url}")

        # URLの正規化とvideo_idの取得
        url, video_id = normalize_youtube_url(url)
        print(f"Normalized URL: {url}")

        if not video_id:
            return jsonify({"error": "Invalid YouTube URL"}), 400

        # YouTube Data APIのセットアップ
        api_key = os.environ.get("YOUTUBE_API_KEY")
        if not api_key:
            return jsonify({"error": "API key not configured"}), 500

        # cache_discovery=False を追加
        youtube = build("youtube", "v3", developerKey=api_key, cache_discovery=False)

        # ビデオ情報の取得
        video_response = youtube.videos().list(part="snippet", id=video_id).execute()

        if not video_response["items"]:
            return jsonify({"error": "Video not found"}), 404

        # タイトルと説明の取得
        video_data = video_response["items"][0]["snippet"]
        title = video_data["title"]
        description = video_data["description"]

        # 字幕の取得（既存のコード）
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        if "ja" in [transcript.language_code for transcript in transcript_list]:
            transcript = transcript_list.find_transcript(["ja"])
        else:
            transcript = transcript_list.find_transcript(["en"])

        full_text = f"動画タイトル: {title}\n動画概要欄: {description}\n動画リンク: {url}\n\n動画文字起こし:\n"

        # 字幕テキストの追加
        for tr in transcript.fetch():
            full_text += tr["text"] + " "

        response = jsonify({"transcript": full_text})
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500
