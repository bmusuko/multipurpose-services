import requests
from bs4 import BeautifulSoup
from flask import Flask, json, request
import random
from dotenv import load_dotenv
import urllib.parse
import logging
import instaloader
from TikTokApi import TikTokApi
from api.ddg import search
from api.tiktok import getPost

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

MAX_POST = 10
L = instaloader.Instaloader()

api = TikTokApi.get_instance(use_selenium=True, use_test_endpoints=True)

app = Flask(__name__)


@app.route("/")
def summary():
    page = requests.get("https://www.kompas.com/covid-19").text.encode("utf-8")
    soup = BeautifulSoup(page, "html.parser")
    # covid summary
    summary = soup.find("div", {"class": "covid__summary"})

    cells = summary.findAll("div")
    confirm, up, _ = cells[1].text[13:].replace(",", "").split(" ")
    confirm = int(confirm)
    up = int(up[1:])

    rawat = int(cells[2].text.split(" ")[0][7:].replace(",", ""))
    meninggal = int(cells[3].text.split(" ")[0][9:].replace(",", ""))
    sembuh = int(cells[4].text.split(" ")[0][6:].replace(",", ""))

    summary_response = {
        "up": up,
        "confirm": confirm,
        "death": meninggal,
        "recovered": sembuh,
        "hospitalized": rawat,
    }
    logger.info(f"get corona summary {up} {confirm} {meninggal} {sembuh} {rawat}")
    response = app.response_class(
        response=json.dumps(summary_response), status=200, mimetype="application/json"
    )
    return response


@app.route("/detail")
def detail():
    page = requests.get("https://www.kompas.com/covid-19").text.encode("utf-8")
    soup = BeautifulSoup(page, "html.parser")
    # covid summary
    cities = []
    tables = soup.find("div", {"class": "covid__table"})

    for table in tables.findAll("div", {"class": "covid__row"}):
        city = table.find("div", {"class": "covid__prov"}).text
        strongs = table.findAll("strong")
        confirm = int(strongs[0].text)
        death = int(strongs[1].text)
        recovered = int(strongs[2].text)

        city_detail = {
            "city": city,
            "confirm": confirm,
            "death": death,
            "recovered": recovered,
        }
        cities.append(city_detail)
    logger.info(f"get corona detail")
    response = app.response_class(
        response=json.dumps(cities), status=200, mimetype="application/json"
    )
    return response


@app.route("/ig")
def ig():
    try:
        username = request.args.get("username")
        profile = instaloader.Profile.from_username(L.context, username)
        # print("get profile")
        if profile.is_private:
            response = app.response_class(status=400, mimetype="application/json")
            return response

        posts = profile.get_posts()
        print("get post")
        count = posts.count
        if count == 0:
            response = app.response_class(status=400, mimetype="application/json")
            return response

        count = min(MAX_POST, count)
        count = random.randint(1, count)
        i = 0
        ret_json = []
        for post in posts:
            print(post)
            i += 1
            # print(f"get post - {i}")

            if i == count:
                caption = post.caption
                typename = post.typename
                if typename == "GraphSidecar":
                    for sidecard in post.get_sidecar_nodes():
                        is_video = sidecard.is_video
                        if is_video:
                            src = sidecard.video_url
                        else:
                            src = sidecard.display_url
                        print(src)
                        ret_json.append({"src": src, "video": is_video})
                else:
                    is_video = post.is_video
                    if is_video:
                        src = post.video_url
                    else:
                        src = post.url
                    ret_json.append({"src": src, "video": is_video})
                break
        # logger.info(f"get ig post {username} {caption} {src}")
        ig_response = {"caption": caption, "result": ret_json}
        response = app.response_class(
            response=json.dumps(ig_response), status=200, mimetype="application/json"
        )

        return response
    except Exception:
        response = app.response_class(status=404, mimetype="application/json")
        return response


@app.route("/igp")
def igp():
    try:
        username = request.args.get("username")

        profile = instaloader.Profile.from_username(L.context, username)

        igp_response = {
            "src": profile.profile_pic_url,
        }
        logger.info(f"get ig profile {username}")
        response = app.response_class(
            response=json.dumps(igp_response), status=200, mimetype="application/json"
        )
        return response
    except Exception:
        response = app.response_class(status=404, mimetype="application/json")
        return response


@app.route("/ddg")
def ddg():
    query = request.args.get("search")
    query = urllib.parse.unquote(query)
    index = request.args.get("index")
    if not index is None:
        try:
            index = int(index)
        except:
            response = app.response_class(status=400, mimetype="application/json")
            return response
    title, src = search(keywords=query, index=index)
    ddg_response = {
        "title": title,
        "src": src,
    }
    response = app.response_class(
        response=json.dumps(ddg_response), status=200, mimetype="application/json"
    )

    return response


@app.route("/tiktok")
def tiktok():
    try:
        username = request.args.get("username")
        caption, url = getPost(api, username)
        if caption == None:
            response = app.response_class(status=400, mimetype="application/json")
            return response

        tiktok_response = {"caption": caption, "url": url}
        logger.info(f"get tiktok post username {username} caption {caption} url {url}")
        response = app.response_class(
            response=json.dumps(tiktok_response),
            status=200,
            mimetype="application/json",
        )
        return response
    except Exception:
        response = app.response_class(status=404, mimetype="application/json")
        return response


if __name__ == "__main__":
    logger.info("Starting application")
    app.run(host="0.0.0.0")
