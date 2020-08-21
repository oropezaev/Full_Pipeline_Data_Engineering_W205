#!/usr/bin/env python
import json
from kafka import KafkaProducer
from flask import Flask, request


print('Starting events')
app = Flask(__name__)
producer = KafkaProducer(bootstrap_servers='kafka:29092')

def log_to_kafka(topic, event):
    event.update(request.headers)
    producer.send(topic, json.dumps(event).encode())

@app.route("/")
def default_response():
    #default_event = {'event_type': 'empty_event'}
    #log_to_kafka('events', default_event)
    return "Default response: No action taken!\n"

@app.route("/purchase")
def default_purchase1():
    return "Warning: No purchase specified!\n"

@app.route("/purchase/<weapon>")
def default_purchase2(weapon):
    return "Warning: No weapon type specified!\n"

@app.route("/purchase/<weapon>/<weapon_type>")
def purchase(weapon,weapon_type):
    purchase_event = {'event_type': 'purchase',
            'item_purchased': weapon,
            'type': weapon_type}
    log_to_kafka('events', purchase_event)
    return weapon_type + ' ' + weapon + ' Purchased!\n'

@app.route('/join_guild')
def join_guild_defult():
    return "Warning: No guild name specified!\n"

@app.route('/join_guild/<guild_name>')
def join_guild(guild_name):
    join_guild_event = {'event_type': 'join_guild',
            'guild_name': guild_name}
    log_to_kafka('events', join_guild_event)
    return "guild joined!\n"

@app.route('/create_guild')
def create_guild_defult():
    return "Warning: No guild name specified!\n"

@app.route('/create_guild/<guild_name>')
def create_guild(guild_name):
    create_guild_event = {'event_type': 'create_guild',
            'guild_name': guild_name}
    log_to_kafka('events', create_guild_event)
    return  "Guild Created: " + guild_name + "\n"
