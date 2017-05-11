#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from datetime import datetime, timedelta
from slacker import Slacker
from flask import Flask, request, json
from pyral import Rally

# Configuration Loading
conf_f = open('.rallyhook.json')
conf_s = conf_f.read()
conf = json.loads(str(conf_s), encoding='utf-8')
conf_f.close()

rally_c = {
    k: v.encode('utf-8') for k, v in conf.get('rally').iteritems()
}
slack_c = {
    k: v.encode('utf-8') for k, v in conf.get('slack').iteritems()
}
rallyhook_c = conf.get('rallyhook')

# API Auth
slack = Slacker(slack_c.get('key'))
rally = Rally(
    server=rally_c.get('server'),
    user=rally_c.get('user'),
    password=rally_c.get('password'),
    apikey=rally_c.get('apikey'),
    workspace=rally_c.get('workspace'),
    project=rally_c.get('project')
)
app = Flask(rallyhook_c.get('appname'))

#Routes
@app.route('/notify/vicaarious', methods = ['POST', 'GET'])
def rallybot():
    app.logger.info(request.headers)
    app.logger.info(request.get_json())
    # if request.headers.get('CONTENT_TYPE', '') == 'application/json':
    return 'hello', 200

if (__name__ == '__main__'):
    app.run(
        host=rallyhook_c.get('host'),
        port=rallyhook_c.get('port'),
        ssl_context=(rallyhook_c.get('cert'), rallyhook_c.get('key')),
        debug=False
    )

# for artifact in response:
#     include = False
#
#     #start building the message string that may or may not be sent up to slack
#     postmessage = '*' + artifact.FormattedID + '*'
#     postmessage = postmessage + ': ' + artifact.Name + '\n';
#     for revision in artifact.RevisionHistory.Revisions:
#         revisionDate = datetime.strptime(revision.CreationDate, '%Y-%m-%dT%H:%M:%S.%fZ')
#         age = revisionDate - datetime.utcnow()
#         seconds = abs(age.total_seconds())
#         #only even consider this story for inclusion if the timestamp on the revision is less than interval seconds old
#         if seconds < interval:
#             description = revision.Description
#             items = description.split(',')
#
#             for item in items:
#                 item = item.strip()
#                 #the only kinds of updates we care about are changes to OWNER and SCHEDULE STATE
#                 #other changes, such as moving ranks around, etc, don't matter so much
#                 #if item.startswith('SCHEDULE STATE ') or item.startswith("OWNER added "):
#
#                 #Modified to push all updates for now
#                 postmessage = postmessage  + "> " + item + ' \n';
#                 print postmessage
#                 include = True
#
#     if include:
#         print "Attempting to send to Slack"
#         postmessage = postmessage + 'https://' + server + '/#/search?keywords=' + artifact.FormattedID + '\n'
#         slack.chat.post_message(channel='aa-bitbucket', text=postmessage, username='aa_rallybot', as_user=True)
#
# print "Rally Slackbot END"
