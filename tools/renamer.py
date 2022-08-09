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

    if data['kind'] in ('proc',):
        tmp[0] = tmp[0].lower()

    result = ''.join(tmp)
    return result


if not os.environ.get("CLANGINCLUDE"):
    raise SystemExit("Define the env var `CLANGINCLUDE`!")

nim_gen = f"""import strutils

import futhark


importc:
  sysPath "{os.environ['CLANGINCLUDE']}"
  path "."

  #[ START OF ALL THE NAMES ]#

"""

for i in data:
    nim_gen += f"  rename \"{i['name']}\", \"{to_nim_case(i)}\"\n"

nim_gen += """\n
  #[ END OF ALL THE NAMES ]#

  "wgpu-native/ffi/wgpu.h"
"""

with open('main.nim', 'w+') as f:
    f.write(nim_gen)
