from flask import Flask
from flask import render_template
import requests
from faker import Faker
import base58
import pandas as pd


app = Flask(__name__)


@app.route("/requirements/")
def requirements():
    with open('requirements.txt') as file:
        requirements = file.read()
        output = render_template('main.html', requirements=requirements)
    return output


@app.route("/generate-users/<int:num_faked>")
def gen_users(num_faked):
    faker = Faker()
    res = []
    for i in range(num_faked):
        res.append(faker.name())
        res.append(faker.email())
        res.append('\n')
    faked = ''.join(str(e) for e in res)
    output = render_template('main.html', faked=faked)
    return output


@app.route("/mean_values")
def mean_values():
    data = pd.read_csv("HW05.csv")
    total_strings = data.shape[0]
    mean_Height = round(data['Height_Inches'].mean()*0.0254, 2)
    mean_Weight = round(data['Weight_Pounds'].mean()*0.45359237, 2)
    res = f'mean_Height is {mean_Height} meters, and mean_Weight is {mean_Weight} kilos, total strings in table - {total_strings}'
    return res


@app.route('/space')
def count_astronauts():
    response = requests.get('http://api.open-notify.org/astros.json').json()
    return f"{response['number']} astronauts are in space"


@app.route('/base58encode/<string>')
def encode(string):
    return base58.b58encode(string)


@app.route('/base58decode/<encoded_string>')
def decode(encoded_string):
    return base58.b58decode(encoded_string)

if __name__ == '__main__':
    app.run()
