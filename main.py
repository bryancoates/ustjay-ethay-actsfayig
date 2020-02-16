""" Creates a web service to convert a random fact to pig latin """

import os

import requests
from flask import Flask, send_file, Response
from bs4 import BeautifulSoup

PIG_URL = "https://hidden-journey-62459.herokuapp.com/piglatinize/"

app = Flask(__name__)

def get_fact():
    """ Gets a random fact from unkno.com """

    response = requests.get("http://unkno.com")

    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("div", id="content")

    return facts[0].getText()

def latinize(fact):
    """ Convert a string to pig latin via POST to site """

    input_text = {'input_text':fact}

    response = requests.post(PIG_URL, input_text, allow_redirects=False)
    url = response.headers.get('Location')

    return url

def get_latin_fact(url):
    """ Gets pig latin fact from web service """

    response = requests.get(url)

    soup = BeautifulSoup(response.content, "html.parser")
    header = soup.find_all("h2")
    latin_fact = header[0].next_sibling

    return latin_fact

@app.route('/')
def home():
    """ Defines the homepage for the site """

    fact = get_fact()
    url = latinize(fact)
    latin_fact = get_latin_fact(url)

    output = f'<ul><b>Random Fact:</b> {fact}</ul> \
    <ul><b>Pig Latin Fact:</b> {latin_fact}</ul> \
    <ul><b>Pig Latin URL:</b> <a href={url}>{url}</a></ul>'

    return output

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='0.0.0.0', port=port)
