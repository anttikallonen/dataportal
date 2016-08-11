from flask import Blueprint, request
from flask import redirect, url_for, current_app, jsonify
from flask_login import login_required, current_user
from flask_application.source.w2e.w2ecommander import commander
from flask_application.source.models import sourcedb, Source, ACTIVE_KEY
import json

__author__ = "Antti Kallonen"
__copyright__ = "Copyright 2015, Tampere University of Technology"
__version__ = "0.1"
__email__ = "antti.kallonen@tut.fi"

SOURCE_ID = 'w2ewithings'
source = Blueprint(SOURCE_ID, __name__)

@source.route('/callback/' + SOURCE_ID, methods=['GET'])
@login_required
def callback():
    parameters = request.args
    current_app.logger.info("User ({0}) returned to callback for device ({1}). Callback parameters ({2})"
                            .format(current_user.get_id(), SOURCE_ID, json.dumps(parameters)))
    # Activate source here
    sourceobject = sourcedb.get_source_for_user(current_user.get_id(), SOURCE_ID)
    if sourceobject.as_dto():
        sourceobject.set_data(ACTIVE_KEY, 'true')
        sourcedb.set_source_for_user(current_user.get_id(), sourceobject)
    return redirect(current_app.config['MY_URL'])


@source.route('/link/' + SOURCE_ID, methods=['GET'])
@login_required
def link():
    current_app.logger.info("User ({0}) requested linking for device ({1})"
                            .format(current_user.get_id(), SOURCE_ID))
    tokens = sourcedb.get_source_for_user(current_user.get_id(), SOURCE_ID).as_dto()
    if not tokens:
        tokens = commander.createUser()
        newsource = Source(dict())
        newsource.set_id(SOURCE_ID)
        newsource.set_values(tokens)
        newsource.set_data(ACTIVE_KEY, 'false')
        sourcedb.set_source_for_user(current_user.get_id(), newsource)
    devicelinks = commander.getUserDeviceLinks(tokens["username"],
                                                   tokens["access_token"])
    deviceShortcutLink = devicelinks["link_url_shortcuts"]["withings"]
    authurl = deviceShortcutLink + "&callback=" + current_app.config['MY_URL'] + '/callback/' + SOURCE_ID
    return redirect(authurl, code=302)


@source.route('/api/source/' + SOURCE_ID + '/disable', methods=['DELETE'])
@login_required
def disable():
    current_app.logger.info("User ({0}) disabled source ({1})"
                            .format(current_user.get_id(), SOURCE_ID))
    sourceobject = sourcedb.get_source_for_user(current_user.get_id(), SOURCE_ID)
    if sourceobject.as_dto():
        commander.deleteUser(sourceobject.get_data('username'), sourceobject.get_data('access_token'))
        sourcedb.del_source_from_user(current_user.get_id(), SOURCE_ID)
    return "DISABLED_" + SOURCE_ID
