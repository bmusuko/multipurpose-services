from TikTokApi import TikTokApi
import logging
import random
import requests

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
did = str(random.randint(10000, 999999999))


def getPost(api, username, results=10):
    logger.info(f"Get tiktok with username: {username}")

    try:
        posts = api.byUsername(
            username=username,
            count=results,
            proxy=None,
            custom_verifyFp="",
            custom_did=did,
        )
        index = random.randint(0, min(results, len(posts)) - 1)
        if index < 0:
            return None, None
        # logger.info(f"post {posts[index]}")
        caption = posts[index]["desc"]
        b = api.get_Video_By_TikTok(
            posts[index], proxy=None, custom_verifyFp="", custom_did=did
        )
        f = open(f"{did}.mp4", "wb")
        f.write(b)
        f.close()
        return caption, "aya,"
    except:
        return None, None
    # except:


# If playwright doesn't work for you try to use selenium
