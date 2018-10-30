"""
Make ajax requests to the ArangoDB server.
"""
import requests
import os

db_url = os.environ.get('DB_URL', 'http://localhost:8529')
db_user = os.environ.get('DB_USER', 'root')
db_pass = os.environ.get('DB_PASS', 'password')


def arango_server_status():
    """Get the status of our connection and authorization to the ArangoDB server."""
    try:
        resp = requests.get(db_url + '/_api/endpoint', auth=(db_user, db_pass))
    except requests.exceptions.ConnectionError:
        return 'no_connection'
    if resp.ok:
        return 'connected_authorized'
    elif resp.status_code == 401:
        return 'unauthorized'
    else:
        return 'unknown_failure'


def bulk_import(data, query):
    """Make a generic arango post request."""
    resp = requests.post(
        db_url + '/_api/import',
        data=data,
        auth=(db_user, db_pass),
        params=query
    )
    if not resp.ok:
        raise ArangoServerError(resp.text)
    return resp.text


class ArangoServerError(Exception):
    """A request to the ArangoDB server has failed (non-2xx)."""

    def __init__(self, resp_text):
        self.resp_text = resp_text

    def __str__(self):
        return '\n'.join([
            '-' * 80,
            'ArangoDB server error',
            self.resp_text,
            '-' * 80
        ])