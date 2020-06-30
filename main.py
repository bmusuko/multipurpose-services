import requests
from bs4 import BeautifulSoup
from flask import Flask, json, request
import random
app = Flask(__name__)


@app.route("/")
def summary():
    page = requests.get('https://www.kompas.com/covid-19').text.encode('utf-8')
    soup = BeautifulSoup(page, "html.parser")
    # covid summary
    summary = soup.find("div", {"class": "covid__summary"})

    cells = summary.findAll("div")
    confirm, up, _ = cells[1].text[13:].replace(',', '').split(' ')
    confirm = int(confirm)
    up = int(up[1:])

    rawat = int(cells[2].text.split(' ')[0][7:].replace(',', ''))
    meninggal = int(cells[3].text.split(' ')[0][9:].replace(',', ''))
    sembuh = int(cells[4].text.split(' ')[0][6:].replace(',', ''))

    summary_response = {
        "up": up,
        "confirm": confirm,
        "death": meninggal,
        "recovered": sembuh,
        "hospitalized": rawat
    }
    response = app.response_class(
        response=json.dumps(summary_response),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route("/detail")
def detail():
    page = requests.get('https://www.kompas.com/covid-19').text.encode('utf-8')
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
            "recovered": recovered
        }
        cities.append(city_detail)

    response = app.response_class(
        response=json.dumps(cities),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route("/ig")
def ig():
    username = request.args.get('username')
    page = requests.get(
        f'https://imginn.com/{username}/').text.encode('utf-8')
    soup = BeautifulSoup(page, "html.parser")
    images = soup.findAll("div", {"class": "img"})[1:]
    if(len(images) == 0):
        print('can\'t get photo')
        response = app.response_class(
            status=400,
            mimetype='application/json'
        )

    else:
        image = random.choice(images)
        img = image.find("img")
        ig_response = {
            "caption": img['alt'],
            "photo": img['data-src']
        }
        response = app.response_class(
            response=json.dumps(ig_response),
            status=200,
            mimetype='application/json'
        )
    return response


@app.route("/igp")
def igp():
    username = request.args.get('username')
    page = requests.get(
        f'https://imginn.com/{username}/').text.encode('utf-8')
    soup = BeautifulSoup(page, "html.parser")
    image = soup.find("div", {"class": "img"})
    if(image == None):
        response = app.response_class(
            status=400,
            mimetype='application/json'
        )
        return response
    else:
        img = image.find("img")
        igp_response = {
            "src": img['src'],
        }
        response = app.response_class(
            response=json.dumps(igp_response),
            status=200,
            mimetype='application/json'
        )
        return response


if __name__ == "__main__":
    app.run(host='0.0.0.0')
