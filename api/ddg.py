import requests
import re
import json
import time
import logging
import random

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def search(keywords, max_results=None, index=None):
    url = "https://duckduckgo.com/"
    params = {"q": keywords}

    logger.debug("Hitting DuckDuckGo for Token")

    #   First make a request to above URL, and parse out the 'vqd'
    #   This is a special token, which should be used in the subsequent request
    res = requests.post(url, data=params)
    searchObj = re.search(r"vqd=([\d-]+)\&", res.text, re.M | re.I)

    if not searchObj:
        logger.error("Token Parsing Failed !")
        return -1

    logger.debug("Obtained Token")

    headers = {
        "authority": "duckduckgo.com",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "sec-fetch-dest": "empty",
        "x-requested-with": "XMLHttpRequest",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "referer": "https://duckduckgo.com/",
        "accept-language": "en-US,en;q=0.9",
    }

    params = (
        ("l", "us-en"),
        ("o", "json"),
        ("q", keywords),
        ("vqd", searchObj.group(1)),
        ("f", ",,,"),
        ("p", "-1"),
        ("v7exp", "a"),
    )

    requestUrl = url + "i.js"

    logger.debug("Hitting Url : %s", requestUrl)

    try:
        res = requests.get(requestUrl, headers=headers, params=params)
        data = json.loads(res.text)
    except Exception:
        logger.debug("Hitting Url Failure - Sleep and Retry: %s", requestUrl)
        # time.sleep(5)
        # continue
    MAX_DEFAULT = 50
    logger.debug("Hitting Url Success : %s", requestUrl)
    # printJson(data["results"])
    sizeResult = len(data["results"][0])
    randomIndex = random.randint(0, min(MAX_DEFAULT, sizeResult) - 1)
    selected = 0
    if index is None:
        selected = randomIndex
    elif index < 0 or index > sizeResult - 1:
        selected = randomIndex
    else:
        selected = index
    logger.info(f"Get selected index {selected} {randomIndex} {sizeResult}")
    return (
        data["results"][selected]["title"].encode("utf-8"),
        data["results"][selected]["image"],
    )
    # print(())
    # if "next" not in data:
    #     logger.debug("No Next Page - Exiting")
    #     exit(0)

    # requestUrl = url + data["next"]


# def printJson(objs):
#     for obj in objs:
#         print(f"Width {obj['width']}, Height {obj['height']}")
#         print(f"Thumbnail {obj['thumbnail']}")
#         print(f"Url {obj['url']}")
#         print(f"Title {obj['title'].encode('utf-8')}")
#         print(f"Image {obj['image']}")
#         print("__________")


# search("Jennie")
