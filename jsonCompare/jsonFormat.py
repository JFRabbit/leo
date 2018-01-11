import json


def json_format(data):
    return json.dumps(data, sort_keys=True, indent=4, ensure_ascii=False)
