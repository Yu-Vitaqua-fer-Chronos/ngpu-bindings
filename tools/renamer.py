#!/usr/bin/python3

import os
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

    if data.get('kind', '<>') == 'proc':
        tmp[0] = tmp[0].lower()

    result = ''.join(tmp)
    return result


try:
    with open('config.json') as f:
        config = json.load(f)
except FileNotFoundError:
    config = {}


if not os.environ.get("CLANGINCLUDE"):
    raise SystemExit("Define the env var `CLANGINCLUDE`!")

renamed = ''
for i in data:
    renamed += f"  rename \"{i['name']}\", \"{to_nim_case(i)}\"\n"

imports = ''
for i in config.get('imports', []):
    imports += f"import {i}\n"

retyped = ''
for i in config.get('retyped', {}):
    retyped += f"  retype {i}, {config['retyped'][i]}\n"

nim_gen = f"""import strutils

import futhark

{imports}


importc:
  sysPath "{os.environ['CLANGINCLUDE']}"
  path "."

  #[ START OF ALL THE NAMES ]#

{renamed}

  #[ END OF ALL THE NAMES ]#


  #[ START OF RETYPING ]#

{retyped}

  #[ END OF RETYPING ]#


  "wgpu-native/ffi/wgpu.h"
"""

with open('main.nim', 'w+') as f:
    f.write(nim_gen)
