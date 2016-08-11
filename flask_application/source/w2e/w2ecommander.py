#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""w2ecommander.py: W2E command abstraction"""
import logging
import json
import requests
from flask_application import app

__author__ = "Antti Kallonen"
__copyright__ = "Copyright 2015, Tampere University of Technology"
__version__ = "0.1"
__email__ = "antti.kallonen@tut.fi"

class W2ECommander(object):
    """Command W2E"""

    def __init__(self, base_url, client_id, client_secret, logger):
        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.logger = logger

    def createUser(self):
        requesturl = self.base_url + "/api/organization/users"
        data = dict()
        data["client_id"] = self.client_id
        data["client_secret"] = self.client_secret
        createResponse = self._makeRequest(requests.post, requesturl, data=json.dumps(data))
        return createResponse

    def deleteUser(self, username, accesstoken):
        requesturl = self.base_url + "/api/organizations/" + self.client_id + "/users/" + username
        headers = dict()
        headers["Authorization"] = "Bearer " + accesstoken
        deleteResponse = self._makeRequest(requests.post, requesturl, headers=headers)
        return deleteResponse

    def getUserInfo(self, username, accesstoken):
        requesturl = self.base_url + "/api/users/" + username
        headers = dict()
        headers["Authorization"] = "Bearer " + accesstoken
        linksResponse = self._makeRequest(requests.get, requesturl, headers=headers)
        return linksResponse

    def getUserDeviceLinks(self, username, accesstoken):
        requesturl = self.base_url + "/api/organization/users/" + username + "/link_token"
        headers = dict()
        headers["Authorization"] = "Bearer " + accesstoken
        linksResponse = self._makeRequest(requests.post, requesturl, headers=headers)
        return linksResponse

    def _makeRequest(self, requestFunction, requestUrl, headers=dict(), params=dict(), data=dict()):
        headers["Content-Type"] = "application/json"
        self.logger.debug("Making " + requestFunction.__name__ + " request to URL: " + requestUrl)
        self.logger.debug("Request headers: " + str(headers))
        r = requestFunction(requestUrl, headers=headers, params=params, data=data)
        jsondata = r.json()
        self.logger.debug("Got request response: " + str(jsondata))
        return jsondata

commander = W2ECommander(base_url=app.config['W2E_SERVER_URL'],
                         client_id=app.config['W2E_CLIENT_ID'],
                         client_secret=app.config['W2E_CLIENT_SECRET'],
                         logger=app.logger)
