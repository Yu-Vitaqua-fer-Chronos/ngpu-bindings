#!/usr/bin/python3

import os
import shutil
import json

nim_bin_loc = shutil.which('nim')

shutil.rmtree('cache', ignore_errors=True)
os.system(nim_bin_loc+' c --nimcache:cache main.nim')

for file in os.listdir('cache'):
    if file.endswith('.json') and file.startswith('opir_'):
        json_file = os.path.join('cache', file)
    if file.endswith('.nim') and file.startswith('futhark_'):
        nim_file = os.path.join('cache', file)

with open(json_file) as f:
    tmp = json.load(f)

data = []

for elem in tmp:
    if 'wgpu' in elem['file']:
        data.append(elem)

with open('output.json', 'w+') as f:
    json.dump(data, f, indent=2)

shutil.copyfile(nim_file, 'futharkwgpu.nim')