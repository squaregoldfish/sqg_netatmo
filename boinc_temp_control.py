import subprocess
import json
import sys
import os

LIMIT=22

def boinc_run_mode(mode):
  password = sys.argv[1]
  command = f'boinccmd --host localhost --passwd {password} --set_run_mode {mode} 0'
  subprocess.call(command, shell=True)

with open('weather.json', 'r') as f:
  json = json.loads(f.read())

indoor_temp = json['Kitchen']['temperature']

if indoor_temp > LIMIT or os.path.exists('STOP'):
  boinc_run_mode('never')
else:
  boinc_run_mode('auto')
