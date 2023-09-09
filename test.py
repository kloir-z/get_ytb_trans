import requests

def call_get_ytb_trans(youtube_url):
    endpoint = "https://asia-northeast2-my-pj-20230703.cloudfunctions.net/get_ytb_trans"
    params = {"url": youtube_url}
    response = requests.get(endpoint, params=params)

    if response.status_code == 200:
        data = response.json()
        return data['transcript']
    else:
        return f"Error: {response.status_code}, {response.text}"

# 例としてのYouTube URLをここに入れる
youtube_url = "https://youtu.be/6JLcPryAPTQ"
result = call_get_ytb_trans(youtube_url)
print(result)

# 【実行例】
# > python .\test.py 
# 動画タイトル: 【苦戦】日本は、世界一厳しい市場？イオンが賭ける謎のネットスーパー（Amazon／イトーヨーカドー／宅配）解説:冨岡久美子
# 動画概要欄: 👇冨岡記者の詳しい解説記事はこちら【独占】イオンが賭ける「謎のECスーパー」に迫るhttps://bit.ly/3QsgNge【解説】ECスーパー成功のために大事な超基本的なことhttps://bit.ly/47hkF9I世界で最もネットスーパーの展開が難しい日本。そんな中、7月10日にイオンのネットスーパー 「...
# 動画リンク: https://youtu.be/6JLcPryAPTQ
# 
# 動画文字起こし:
# 野菜とかで一番出るじゃないですかその ネットスーパーの実力ってそもそも日本 だけじゃなく.......