from TikTokApi import TikTokApi
import random
import requests
import sys

api = TikTokApi.get_instance(use_selenium=True, use_test_endpoints=True)
did = str(random.randint(10000, 999999999))
# tiktoks = api.trending(proxy=None, custom_verifyFp="")
results = 10

username = sys.argv[1] or "bp_tiktok"
# b = api.get_Video_By_TikTok(tiktoks[0])
tiktoks = api.byUsername(
    username=username, count=results, proxy=None, custom_verifyFp="", custom_did=did
)
# url = f"https://www.tiktok.com/@{posts[0]['author']['uniqueId']}/video/{posts[0]['id']}?lang=en"
# print(url)
# print(posts[0])
# b = api.get_Video_By_TikTok(posts[0])
# b = api.get_Video_By_DownloadURL(
#     posts[0]["video"]["downloadAddr"], language="en", proxy=None, custom_verifyFp=""
# )
# b = api.get_Video_By_Url(url, return_bytes=0, custom_verifyFp="")
# video_bytes = requests.get(
#     posts[0]["video"]["downloadAddr"], headers={"User-Agent": "okhttp"}
# ).content
# print(video_bytes)

for tiktok in tiktoks:
    b = api.get_Video_By_TikTok(tiktok, proxy=None, custom_verifyFp="", custom_did=did)
    f = open(f"{did}.mp4", "wb")
    f.write(b)
    f.close()
    print(tiktok)
    break