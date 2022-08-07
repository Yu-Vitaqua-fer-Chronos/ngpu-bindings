#!/usr/bin/python3
import sys
import json


with open(sys.argv[1]) as f:
    tmp = json.load(f)

data = []

for elem in tmp:
    if 'wgpu' in elem['file']:
        data.append(elem)

with open('output.json', 'w+') as f:
    json.dump(data, f, indent=2)
