import datetime
from dateutil.tz import tzutc
import json
import traceback
from aws_metrics_collector import LogWrapper
from aws_metrics_collector import get_utc_timestamp


def convert_unknown_obj(unknown_obj):
    if isinstance(unknown_obj, (datetime.date, datetime.datetime)):
        return unknown_obj.timestamp()
    else:
        return '{}'.format(unknown_obj)


def dict_to_json(dict_obj: dict, log_wrapper: LogWrapper=LogWrapper())->str:
    final_str = ''
    try:
        if isinstance(dict_obj, dict):
            final_str = json.dumps(dict_obj, default=convert_unknown_obj, indent=4, sort_keys=True)
        else:
            log_wrapper.error(message='dict_obj incorrect type: {}'.format(type(dict_obj)))
    except:
        log_wrapper.error(message='EXCEPTION: {}'.format(traceback.format_exc()))
    return final_str

# EOF
