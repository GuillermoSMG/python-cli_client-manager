import json_mng

my_data = json_mng.read_json()


def get(data):
    return data[len(data) - 1]['id']
