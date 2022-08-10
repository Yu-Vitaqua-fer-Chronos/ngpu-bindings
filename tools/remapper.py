#!/usr/bin/python3

import json
import re

CS = re.compile(r"[\\-_/]|(?<![A-Z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])")

with open('opir.json') as f:
    opir = json.load(f)

replacements = {}

'''
def to_nim_case(data):
    name = data['name']
    tmp = CS.split(name.replace('_', ''))
    splitcase = [c for c in tmp if c != '']

    tmp = []
    prefix = "wgpu".title()
    for text in splitcase:
        if text.title() == prefix:
            pass
        else:
            tmp.append(text.title())

    if data['kind'] == 'proc':
        tmp[0] = tmp[0].lower()
    if data['kind'] == 'enum':
        for _ in data['fields']:
            name = _['name']
            temp = CS.split(name.replace('_', ''))
            splitcase = [c for c in temp if c != '']
            temp = []

            for text in splitcase:
                if text.title() == prefix:
                    pass
                else:
                    temp.append(text.title())

                    n = ''.join(temp)
                    replacements['Wgpu'+n.lower()] = n

    result = ''.join(tmp)
    return result
'''

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

    if data.get('kind', '<>') == 'proc':
        tmp[0] = tmp[0].lower()
    elif data.get('kind', '<>') == 'enum':
        for f in data['fields']:
            n = to_nim_case(f)
            replacements['Wgpu'+n.lower()] = n

    result = ''.join(tmp)
    return result


for i in opir:
    _ = to_nim_case(i)
    bname = _
    nname = _

    if i['kind'] == 'proc':
        bname = bname.lower()
    else:
        bname = bname.lower()
        bname = bname[0].upper() + bname[1:]

    replacements[bname] = nname


with open('futharkwgpu.nim') as f:
    text = f.read()
    for r in replacements:
        text = text.replace(r, replacements[r])

with open('futharkwgpu.nim', 'w+') as f:
    f.write(text)
