#!/usr/bin/env python3.9

from flask import Flask, render_template, request, send_file
from flask_pymongo import PyMongo
import os
import datetime

app = Flask(__name__)

#setup mongo connection
app.config['MONGO_URI']="mongodb://localhost:27017/shows_db"
mongo = PyMongo(app)

#connect to collection
tv_shows = mongo.db.tv_shows

#READ
@app.route("/")
def index():
    #find all 
    all_shows = list(tv_shows.find())

    return render_template("index.html", data=all_shows)

#CREATE
@app.route("/create", methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        form_url = os.path.join(app.template_folder, "", 'form.html')
        return send_file(form_url, etag='create')
    else:
        name = request.form['name']
        seasons = request.form['seasons']
        duration = request.form['duration']
        year = request.form['year']
        date_added = datetime.datetime.utcnow()
        post_data = {'name': name, 'seasons': seasons, 'duration':duration, 'year':year, 'date_added': date_added}
        tv_shows.insert_one(post_data)

        text_success = "Data successfully added: " + str(post_data)
        #return render_template('index.html', data=text_success)
        return text_success

#UPDATE
@app.route("/update", methods=['GET', 'POST'])
def update():
    if request.method == 'GET':
        form_url = os.path.join(app.template_folder, "", 'form.html')
        return send_file(form_url)
    else:
        name = request.form['name']
        seasons = request.form['seasons']
        duration = request.form['duration']
        year = request.form['year']
        #date_added = datetime.datetime.utcnow()
        post_data = {name, seasons, duration, year}
        filter = {'name': name}
        add = {}
        if seasons != '' and seasons is not None:
            add['seasons'] = seasons
        if year != '' and year is not None:
            add['year'] = year
        if duration != '' and duration is not None:
            add['duration'] = duration
        
        new_values = {'$set': add}
        tv_shows.update_one(filter, new_values)

        text_success = "Data successfully updated: " + str(post_data)
        #return render_template('index.html', data=text_success)
        return text_success

#DELETE
@app.route("/delete", methods=['GET', 'POST'])
def delete():
    if request.method == 'GET':
        form_url = os.path.join(app.template_folder, "", 'form.html')
        return send_file(form_url)
    else:
        name = request.form['name']
        tv_shows.delete_one({'name': name})
        text_success = "Data successfully updated: " + str(name)
        return render_template('index.html', data=text_success)


if __name__ == "__main__":
    app.run(debug=True)