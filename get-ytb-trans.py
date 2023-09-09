from youtube_transcript_api import YouTubeTranscriptApi
import re
import requests
from bs4 import BeautifulSoup
from flask import escape, request, jsonify

def get_transcript(request):
    url = request.args.get('url')
    # Check if the clipboard content is a YouTube URL
    if not re.match(r'(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+$', url):
        return "Invalid YouTube URL. Please provide a valid YouTube URL."

    # Extract video id from the url
    if "youtu.be" in url:
        video_id = url.split("/")[-1]
    else:  # assuming it's a "youtube.com" url
        video_id = url.split("v=")[-1]

    # Fetch the page content
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    # Extract title and description
    title = soup.find('meta', property='og:title')
    description = soup.find('meta', property='og:description')
    if title and description:
        title, description = title["content"], description["content"]
    else:
        return "Could not fetch title and description."

    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

    # Check if there's a Japanese transcript, otherwise use English
    if 'ja' in [transcript.language_code for transcript in transcript_list]:
        transcript = transcript_list.find_transcript(['ja'])
    else:
        transcript = transcript_list.find_transcript(['en'])

    full_text = f"動画タイトル: {title}\n動画概要欄: {description}\n動画リンク: {url}\n\n動画文字起こし:\n"

    # Check the language of the transcript and append text accordingly
    if transcript.language_code == 'en':
        for tr in transcript.fetch():
            full_text += tr['text'] + " "
    else:
        for tr in transcript.fetch():
            full_text += tr['text'] + " "

    return jsonify({'transcript': full_text})