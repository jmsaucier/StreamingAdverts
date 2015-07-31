from flask import render_template, session
from pymongo import MongoClient
from bson import json_util
from bson import ObjectId
from app import app

@app.route('/marketing')
def marketing():
    try:
        return render_template('marketing.jade')
    except Exception as e:
        print e

@app.route('/marketing_campaigns')
def marketing_campaign():
    client = MongoClient()
    db = client.ads
    collection = db.campaigns
    campaigns = list(collection.find({"username":session["username"]}))
    return json_util.dumps(campaigns)
   
@app.route('/manage_campaign/<oid>')
def manage_campaign(oid):
    client = MongoClient()
    db = client.ads
    collection = db.campaigns
    campaign = collection.find_one({"username":session["username"], "_id": ObjectId(oid)})
    return json_util.dumps(campaign)