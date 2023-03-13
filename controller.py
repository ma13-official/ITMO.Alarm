from flask import Flask, request
import logging

app = Flask(__name__)


@app.route("/create", methods={"POST"})
def create():
    response = {
        "version": request.json["version"]
    }


@app.route("/edit", methods={"POST"})
def edit():
    response = {
        "version": request.json["version"]
    }


