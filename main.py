# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template

from instance.config import DevelopmentConfig


app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.config.from_object(DevelopmentConfig)

@app.route('/')
def hello():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=8000)