from youtube_transcript_api import YouTubeTranscriptApi
from flask import jsonify
from urllib.parse import urlparse, parse_qs
from googleapiclient.discovery import build  # type: ignore
import os
import sys
import platform


def normalize_youtube_url(url):
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
        print(f"Python version: {sys.version}")
        print(f"Platform: {platform.platform()}")

        url = request.args.get("url")
        print(f"Received URL: {url}")

        url, video_id = normalize_youtube_url(url)
        print(f"Normalized URL: {url}")
        print(f"Video ID: {video_id}")

        if not video_id:
            return jsonify({"error": "Invalid YouTube URL"}), 400

        # YouTube Data APIのセットアップ
        api_key = os.environ.get("YOUTUBE_API_KEY")
        if not api_key:
            return jsonify({"error": "API key not configured"}), 500

        youtube = build("youtube", "v3", developerKey=api_key, cache_discovery=False)

        # まず動画の情報を取得
        video_response = youtube.videos().list(part="snippet", id=video_id).execute()

        if not video_response["items"]:
            return jsonify({"error": "Video not found"}), 404

        video_data = video_response["items"][0]["snippet"]
        title = video_data["title"]
        description = video_data["description"]

        # 字幕トラックの一覧を取得
        print("Fetching caption tracks...")
        captions_response = youtube.captions().list(part="snippet", videoId=video_id).execute()

        print(f"Captions response: {captions_response}")

        # 字幕情報の取得を試みる
        transcript_text = ""
        try:
            if "items" in captions_response and captions_response["items"]:
                print("Caption tracks found in YouTube Data API")
                # YouTube Transcript APIで字幕取得を試みる
                transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

                if "ja" in [t.language_code for t in transcript_list]:
                    print("Japanese transcript found")
                    transcript = transcript_list.find_transcript(["ja"])
                else:
                    print("Using English transcript")
                    transcript = transcript_list.find_transcript(["en"])

                transcripts = list(transcript.fetch())
                print("Successfully fetched transcript")

                transcript_text = "\n\n動画文字起こし:\n"
                for tr in transcripts:
                    transcript_text += tr["text"] + " "
            else:
                print("No caption tracks found")
                transcript_text = "\n\n※この動画には字幕が設定されていません。"

        except Exception as transcript_error:
            print(f"Transcript error details: {type(transcript_error).__name__}: {str(transcript_error)}")
            transcript_text = "\n\n※字幕の取得に失敗しました。"

        # 動画情報と字幕を組み合わせる
        full_text = f"動画タイトル: {title}\n動画概要欄: {description}\n動画リンク: {url}{transcript_text}"

        response = jsonify({"transcript": full_text})
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response

    except Exception as e:
        print(f"Error type: {type(e).__name__}")
        print(f"Error details: {str(e)}")
        return jsonify({"error": str(e)}), 500
