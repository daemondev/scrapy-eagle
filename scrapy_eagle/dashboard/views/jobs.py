import json
from collections import OrderedDict
from datetime import datetime

import flask

from scrapy_eagle.dashboard import settings
from scrapy_eagle.dashboard.memory import get_job_object


jobs = flask.Blueprint('jobs', __name__)


@jobs.route('/list')
def listing():

    _spiders = settings.get_spiders()

    # May happen to request this route before we've
    # the settings filled by the gevent async execution `green_threads.find_new_spiders`
    if not _spiders:
        return flask.Response(
            response=json.dumps({}, sort_keys=True),
            status=200,
            mimetype="application/json"
        )

    _spiders.sort()

    d = OrderedDict()

    for s in _spiders:

        obj = get_job_object(key=s)

        if obj:
            d[s] = obj
        else:
            # TODO: How to proceed for newly jobs
            pass

        # d[s] = {}
        # d[s]['active'] = True
        # d[s]['job_type'] = 'spider' # or 'command'
        # d[s]['min_concurrency'] = 1
        # d[s]['max_concurrency'] = 5
        # d[s]['max_memory_mb'] = 200
        # d[s]['priority'] = 7
        # d[s]['frequency_minutes'] = 60
        # d[s]['last_started_at'] = 20
        # d[s]['start_urls'] = []
        # d[s]['last_started_at'] = datetime.utcnow().isoformat()

    # TODO: Iterate over all commands
    obj = get_job_object(key='generator')

    if obj:
        d['generator'] = obj

    # d['generator'] = {}
    # d['generator']['active'] = True
    # d['generator']['job_type'] = 'command'  # or 'command'
    # d['generator']['min_concurrency'] = 1
    # d['generator']['max_concurrency'] = 3
    # d['generator']['max_memory_mb'] = 50
    # d['generator']['priority'] = 2
    # d['generator']['frequency_minutes'] = 5
    # d['generator']['last_started_at'] = 20
    # d['generator']['start_urls'] = None

    return flask.Response(
        response=json.dumps(d, sort_keys=True),
        status=200,
        mimetype="application/json"
    )