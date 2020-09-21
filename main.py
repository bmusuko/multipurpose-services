import requests
from bs4 import BeautifulSoup
from flask import Flask, json, request
import random
from dotenv import load_dotenv

# import os
import instaloader

# load_dotenv()

# USER = os.getenv("USERNAME")
# PASSWORD = os.getenv("PASSWORD")
MAX_POST = 20
L = instaloader.Instaloader()

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

    response = app.response_class(
        response=json.dumps(cities), status=200, mimetype="application/json"
    )
    return response


@app.route("/ig")
def ig():
    try:
        username = request.args.get("username")

        profile = instaloader.Profile.from_username(L.context, username)
        print("get profile")
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
        for post in posts:
            i += 1
            print(f"get post - {i}")

            if i == count:
                is_video = post.is_video
                if is_video:
                    src = post.video_url
                else:
                    src = post.url
                caption = post.caption
                break

        ig_response = {"caption": caption, "src": src, "video": is_video}
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
        response = app.response_class(
            response=json.dumps(igp_response), status=200, mimetype="application/json"
        )
        return response
    except Exception:
        response = app.response_class(status=404, mimetype="application/json")
        return response


if __name__ == "__main__":
    # try:
    # L.load_session_from_file(USER) # (load session created w/
    # except FileNotFoundError:
    # L.login(USER, PASSWORD)
    # L.save_session_to_file()
    # except:
    # print("sumting wong")
    app.run(host="0.0.0.0")
