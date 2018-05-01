''' Exposes REST endpoints to store and retrieve in cache '''
import json
from flask import request
from cache_server import app
from cache_management.cache_agent import CacheAgent
from config import CONFIG

cache = CacheAgent(CONFIG["max_size"])

@app.route('/documents')
def index():
    ''' returns list of available document keys '''
    docs = cache.get_all_keys()
    return json.dumps(docs)

@app.route('/document/<name>')
def get_single_doc(name):
    ''' returns the last known document value '''

    doc = cache.get_document(name)
    if doc is None:
        return json.dumps({
            "status": "error",
            "message": "cannot find the document"
        })
    return json.dumps({
        "key": doc.key,
        "value": doc.get_last_value()
    })

@app.route('/document/<name>/versions')
def get_all_document_versions(name):
    ''' returns all document version for a key '''

    doc = cache.get_document(name)
    if doc is None:
        return json.dumps({
            "status": "error",
            "message": "cannot find the document"
        })
    return json.dumps(doc.get_all_values())

@app.route('/document', methods=["POST"])
def set_document():
    ''' set cache document for a key '''

    insert_request = request.get_json()
    if insert_request is None or insert_request["key"] is None or insert_request["value"] is None:
        return json.dumps({
            "status": "error",
            "message": "Incorrect request. key or value missing"
        }), 422

    cache.set_document(insert_request["key"], insert_request["value"])
    return json.dumps({"success": "true"})

@app.after_request
def apply_caching(response):
    """ CORS policy """
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Origin, Accept, X-Requested-With, Content-Type"
    return response
