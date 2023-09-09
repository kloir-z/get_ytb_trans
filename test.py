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
# 野菜とかで一番出るじゃないですかその ネットスーパーの実力ってそもそも日本 だけじゃなくてその世界中のネット スーパーが難しい [音楽] NewsPicks編集部の富岡です皆 さん普段ネットスーパーで買い物をします かコロナを経てかなり身近になっているん じゃないでしょうか 注文して 商品が すぐ届いてすごい便利だと思うん ですけどその一方で買い物とか 欠品とか買いすぎて冷蔵庫が爆発するとか 消費者のそういう苦労もさることながら ネットスーパーのビジネスというのは 面白いと同時に難しくてAmazonも 結構苦戦してたりしますそんな中で先月 イオンが巨大なネットスーパーを立 ち上げ ましたグリーンビーンズというスーパー です今日はこのグリーンビーズの話を中心 にネットスーパーの裏側について話します 今までのネットスーパーはスーパーの店舗 から直接届いていたんですけれども グリーンビーンズは倉庫から直接 届くシステムになっています現在の対象 地域は都内の一部などちょっと限定的なん ですけれども今後1年で23区全域にまで 拡大し 商品数も約5万点に拡大すると発表してい ますまたグリーンビーンズはイギリスの 大手ネットスーパーオカドと提携してい ます北海道というのはネットスーパー事業 で中核となるテクノロジーを提供して10 カ国以上の主要な小売業に対して今事業を 推進していますリオンのこのネット スーパーは北海道の技術によって何が できるかというと 仙