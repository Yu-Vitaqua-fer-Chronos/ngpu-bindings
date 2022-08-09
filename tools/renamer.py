#!/usr/bin/python3

import json
import re

CS = re.compile(r"[\\-_/]|(?<![A-Z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])")

with open('opir.json') as f:
    data = json.load(f)

def to_nim_case(data):
    name = data['name']
    splitcase = CS.split(name)
    splitcase[:] = [c for c in splitcase if c != '']

    tmp = []
    prefix = "wgpu".title()
    for text in splitcase:
        if text.title() == prefix:
            pass
        else:
            tmp.append(text.title())

    result = ''.join(tmp)
    return result

for i in data:
    print(f"  rename \"{i['name']}\", \"{to_nim_case(i)}\"")
