import hashlib
import hmac
import json
import os

from flask import request

signingSec = os.environ.get('SLACK_SECRET')

def validate_token(fn):
    def _wrap(*args, **kwargs):
        auth_data = _get_auth_data(request)
        if not auth_data:
            return json.dumps({'status_code': 403, 'data': 'Forbidden'})
        return fn(*args, **kwargs)
    _wrap.__name__ = fn.__name__
    return _wrap

def _get_auth_data(req):
    timestamp = request.headers['X-Slack-Request-Timestamp']
    sig_string = 'v0:' + timestamp + ':' + req.get_data().decode('utf8')
    my_signature = 'v0=' + hmac.new(
        bytes(signingSec, 'latin-1'),
        msg=bytes(sig_string, 'latin-1'),
        digestmod=hashlib.sha256
    ).hexdigest()
    slack_signature = request.headers['X-Slack-Signature']
    return hmac.compare_digest(my_signature, slack_signature)
