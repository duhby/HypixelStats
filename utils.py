# dubs#9025
# Hypixel Stats
# 1/31/21

import json

class Files:
    def get_json(path):
        with open(path, 'r') as file:
            data = json.load(file)
        return data

    def write_json(path, data):
        with open(path, 'w') as file:
            json.dump(data, file)