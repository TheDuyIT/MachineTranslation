import os
import sys
sys.path.append(os.getcwd())

from flask import Flask, render_template, request
from wtforms import Form, TextAreaField, validators
from src.test import Test
import pickle
import sqlite3
import os
import numpy as np


app = Flask(__name__, static_folder = "templates")

cur_dir = os.path.dirname(__file__)
translater = Test()


class ReviewForm(Form):
    moviereview = TextAreaField('',
                                [validators.DataRequired()])
                                # ,validators.length(min=10)])

@app.route('/')
def index():
    form = ReviewForm(request.form)
    return render_template(r'reviewform.html', form=form)

@app.route('/results', methods=['POST'])
def results():
    form = ReviewForm(request.form)
    if request.method == 'POST' and form.validate():
        content = request.form['moviereview']
        VN = translater.translate(content)
        return render_template(r'reviewform.html',form=form,
                                content=VN)
    return render_template(r'reviewform.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(port = '8080',host = '0.0.0.0', debug=True)
