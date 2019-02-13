import os
import sys
import requests
from flask import jsonify, request, make_response, send_from_directory

# ENV var: PORT and ENV defined in the docker-compose.yml
# get the dirname of this file == pwd
ROOT_PATH = os.path.dirname(os.path.realpath(__file__))

# py 2 set env var, but not needed
os.environ['ROOT_PATH'] = ROOT_PATH

# add modules dir to PATH env var to be able to ex from pwd
# allows you to directly import every module
sys.path.append(os.path.join(ROOT_PATH, 'modules'))


import logger
from app import app

# TODO analyze
# create a logger obj to log the info and debug
LOG = logger.get_root_logger(os.getenv('ROOT_LOGGER', 'root'), filename=os.path.join(ROOT_PATH, 'output.log'))


# port var to run the server on
PORT=os.getenv('PORT', 4000)


# routes
@app.errorhandler(404)
def not_found(error):
    """ error handler """
    LOG.error(error)
    return make_response(jsonify({'Error you jive turkey': 'Not found'}), 404)


@app.route('/')
def index():
    """ static files serve """
    return send_from_directory('dist', 'index.html')

# TODO what does this route do??
@app.route('/<path:path>')
def static_proxy(path):
    """ static folder server """
    filename = os.path.basename(path)
    # get list with last element rm from path: x = path.split('/')[:-1]
    # build path: '/'.join(x)
    file_name = path.split('/')[-1]
    dirname = os.path.join('dist', '/'.join(path.split('/')[:-1]))
    return send_from_directory(dirname, filename)

if __name__ == '__main__':
    LOG.info(f"running env: {os.environ.get('ENV')}")
    app.config['DEBUG']=os.environ.get('ENV') == 'development'
    app.run(host = '0.0.0.0', port = int(PORT))  # run app
