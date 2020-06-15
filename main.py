import requests
from bs4 import BeautifulSoup
from flask import Flask,json
app = Flask(__name__)

@app.route("/")
def hello():
    page = requests.get('https://www.kompas.com/covid-19').text.encode('utf-8')
    soup = BeautifulSoup(page, "html.parser")
    # covid summary
    summary = soup.findAll("div", {"class": "covid__summary"})[0]
    # summary = soup.findAll("div", {"class": "covid__box2 -cases"})[0]
    cells = summary.findAll("div")


    confirm , up , _=  cells[1].text[13:].replace(',','').split(' ')
    confirm = int(confirm)
    up = int(up[1:])


    rawat = int(cells[2].text.split(' ')[0][7:].replace(',',''))
    meninggal = int(cells[3].text.split(' ')[0][9:].replace(',',''))
    sembuh = int(cells[4].text.split(' ')[0][6:].replace(',',''))

    summary_response = {
        "up" : up,
        "confirm" : confirm,
        "death" : meninggal,
        "recovered":sembuh,
        "hospitalized" : rawat
    }
    response = app.response_class(
        response=json.dumps(summary_response),
        status=200,
        mimetype='application/json'
    )
    return response

if __name__ == "__main__":
    app.run()