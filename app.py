'''
HOW TO SET UP FLASK

1) In terminal
    1.1) set FLASK_APP=app.py
    1.2) set FLASK_ENV=development
2) Run Flask - in terminal: flask run

pip install pymongo[srv]

'''

import datetime
from flask import Flask, render_template, request
from pymongo import MongoClient


def create_app():
    # Has to be this name 
    # Then deployment mechanism will only deploy this app and MongoClient ONCE

    app = Flask(__name__)
    client = MongoClient("mongodb+srv://Julian:valdman11@microbrog-application.tm7r6.mongodb.net/test")
    app.db = client.microblog # cluster name is microblog

    # entries = []

    @app.route("/", methods=["GET", "POST"])
    def home():

        # entries: collection
        # Printing all 
        # print([e for e in app.db.entries.find({})])

        if request.method == "POST":
            # request.form is dictionary
            # here "content" is the name attribute value of the textarea 
            entry_content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
            # entries.append((entry_content, formatted_date))
            
            # INSERT 
            app.db.entries.insert({"content": entry_content, "date": formatted_date})

        entries_with_date = [
            ( 
                entry["content"], 
                entry["date"], 
                datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d")
            )
            for entry in app.db.entries.find({})
        ]

        return render_template("home.html", entries=entries_with_date)

    return app