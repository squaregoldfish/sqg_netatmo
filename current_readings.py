import requests
import toml
import json
from datetime import datetime, timedelta
import pytz
import curses
import time
from threading import Thread
import traceback

ERROR = None

def main(stdscr):
  global ERROR
  keep_running = True

  config = toml.load('readings_config.toml')
  setup_screen(stdscr)

  netatmothread = Thread(target=netatmo_thread, args=[stdscr, config], daemon=True)
  netatmothread.start()

  while keep_running:
    time.sleep(0.1)
    char = ''
    try:
      char = stdscr.getkey()
    except:
      pass

    if char == 'q' or ERROR is not None:
      keep_running = False

def netatmo_thread(stdscr, config):
  stdscr.clear()
  stdscr.addstr(0, 0, 'Fetching data...')
  stdscr.refresh()
  try:
    data_json = None
    while True:
      try:
        response = requests.get(config['readings']['source_url'])
        response.raise_for_status()
        netatmo_json = response.json()['devices'][0]

        modules = {
          netatmo_json['module_name']: netatmo_json['dashboard_data'],
        }

        for m in netatmo_json['modules']:
          modules[m['module_name']] = m['dashboard_data']

        names = {
          'Outdoor Module': 'Outdoor',
          'Main Unit': 'Bedroom',
          'Indoor 1': 'Living Room',
          'Rain': 'Rain'
        }

        timezone = pytz.timezone(netatmo_json['place']['timezone'])

        # Now draw the screen
        stdscr.clear()
        time.sleep(0.1)
        yindex = 0

        observation_time = get_observation_time(netatmo_json, timezone)

        stdscr.addstr(yindex, 0, 'Observation time:')
        stdscr.addstr(yindex + 1, 2, observation_time.strftime('%Y-%m-%d %H:%M:%S %Z'))

        yindex += 3
        stdscr.addstr(yindex, 0, 'Temperature')
        for module in names.keys():
          if 'Temperature' in modules[module]:
            yindex += 1
            stdscr.addstr(yindex, 2, f'{names[module]}: ')
            stdscr.addstr(yindex, 20, f'{modules[module]["Temperature"]:5.1f} °C')

        yindex = yindex + 2
        stdscr.addstr(yindex, 0, 'Humidity')
        for module in names.keys():
          if 'Humidity' in modules[module]:
            yindex += 1
            stdscr.addstr(yindex, 2, f'{names[module]}: ')
            stdscr.addstr(yindex, 20, f'{modules[module]["Humidity"]:3d} %')

        yindex = yindex + 2
        stdscr.addstr(yindex, 0, 'Pressure')
        for module in names.keys():
          if 'Pressure' in modules[module]:
            yindex += 1
            stdscr.addstr(yindex, 2, f'{names[module]}: ')
            stdscr.addstr(yindex, 20, f'{modules[module]["Pressure"]:6.1f} mb')

        yindex = yindex + 2
        stdscr.addstr(yindex, 0, 'Carbon Dioxide')
        for module in names.keys():
          if 'CO2' in modules[module]:
            yindex += 1
            stdscr.addstr(yindex, 2, f'{names[module]}: ')
            stdscr.addstr(yindex, 20, f'{modules[module]["CO2"]:4d} ppm')

        yindex = yindex + 2
        stdscr.addstr(yindex, 0, 'Rain')
        for module in names.keys():
          if 'sum_rain_24' in modules[module]:
            yindex += 1
            stdscr.addstr(yindex, 2, f'{names[module]}: ')
            stdscr.addstr(yindex, 20, f'{modules[module]["sum_rain_24"]:5.1f} mm')

        yindex = yindex + 2
        stdscr.addstr(yindex, 0, 'Battery Levels')
        for module in netatmo_json['modules']:
          if 'battery_percent' in module:
            yindex += 1
            stdscr.addstr(yindex, 2, f'{names[module["module_name"]]}: ')
            stdscr.addstr(yindex, 20, f'{module["battery_percent"]: 3d} %')

        observation_delta = timedelta(minutes=1, seconds=1)
        next_get_time = datetime.now().astimezone() + observation_delta
        sleep_time = (next_get_time - datetime.now().astimezone()).total_seconds()
        if sleep_time < 0:
          sleep_time = 60

        yindex += 2
        stdscr.addstr(yindex, 0, 'Next retrieval time:')
        stdscr.addstr(yindex + 1, 2, next_get_time.strftime('%Y-%m-%d %H:%M:%S %Z'))

        stdscr.refresh()

        time.sleep(sleep_time)
      except Exception as e:
        print(e)
        print(data_json)
        print(traceback.format_exc())
        time.sleep(300)
  except:
    global ERROR
    ERROR = traceback.format_exc()

def setup_screen(stdscr):
  # Clear screen
  stdscr.nodelay(1)

  # Hide the cursor
  curses.curs_set(0)

def build_json(data):
  output = {}

  station = data[0]

  timezone = pytz.timezone(station['place']['timezone'])

  # Main module
  output[get_module_name(station)] = get_module_data(station, timezone)

  for module in station['modules']:
    if module['reachable']:
      output[get_module_name(module)] = get_module_data(module, timezone)

  return output

def get_observation_time(data, timezone):
  utc_time = data['dashboard_data']['time_utc']
  return datetime.fromtimestamp(utc_time, tz=timezone)


curses.wrapper(main)
if ERROR is not None:
  print(f'{ERROR}')
