#!/usr/bin/env python
from requests_futures.sessions import FuturesSession
import json

session = FuturesSession()

def below_volume_threshold(threshold):
    session.post('http://kraken.test.io/events', data=json.dumps({ 'event': { 'name': 'below_volume_threshold', 'payload': { 'threshold': threshold } } }))

def over_volume_threshold(threshold):
    session.post('http://kraken.test.io/events', data=json.dumps({ 'event': { 'name': 'over_volume_threshold', 'payload': { 'threshold': threshold } } }))
