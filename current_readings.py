import requests
import toml
import netatmo
import json
from datetime import datetime
import pytz
import curses
import time
from threading import Thread
import traceback

UPDATE_INTERVAL = 15 #minutes
ERROR = None

def main(stdscr):
  global ERROR
  keep_running = True

  config = toml.load('config.toml')
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
    station = netatmo.WeatherStation(config['netatmo'])

    while True:
      station.get_data()
      weather_data = station.devices
      data_json = build_json(weather_data)
      with open('weather.json', 'w') as f:
        json.dump(data_json, f)

      #with open('weather.json', 'r') as f:
      #  data_json = json.load(f)

      # Now draw the screen
      stdscr.clear()
      time.sleep(0.1)
      yindex = 0

      stdscr.addstr(yindex, 0, 'Observation time:')
      stdscr.addstr(yindex, 18, data_json['Kitchen']['time'])

      yindex += 2
      stdscr.addstr(yindex, 0, 'Temperature')
      for device in data_json:
        if 'temperature' in data_json[device]:
          yindex += 1
          stdscr.addstr(yindex, 2, f'{device}: ')
          stdscr.addstr(yindex, 20, f'{data_json[device]["temperature"]:5.1f} °C')

      yindex = yindex + 2
      stdscr.addstr(yindex, 0, 'Humidity')
      for device in data_json:
        if 'humidity' in data_json[device]:
          yindex += 1
          stdscr.addstr(yindex, 2, f'{device}: ')
          stdscr.addstr(yindex, 22, f'{data_json[device]["humidity"]: 3d}  %')

      yindex = yindex + 2
      stdscr.addstr(yindex, 0, 'Pressure')
      for device in data_json:
        if 'pressure' in data_json[device]:
          yindex += 1
          stdscr.addstr(yindex, 2, f'{device}: ')
          stdscr.addstr(yindex, 19, f'{data_json[device]["pressure"]:6.1f} mb')

      yindex = yindex + 2
      stdscr.addstr(yindex, 0, 'Carbon Dioxide')
      for device in data_json:
        if 'co2' in data_json[device]:
          yindex += 1
          stdscr.addstr(yindex, 2, f'{device}: ')
          stdscr.addstr(yindex, 20, f'{data_json[device]["co2"]: 4d} ppm')

      yindex = yindex + 2
      stdscr.addstr(yindex, 0, 'Rain')
      for device in data_json:
        if 'rain24' in data_json[device]:
          yindex += 1
          stdscr.addstr(yindex, 2, f'{device}: ')
          stdscr.addstr(yindex, 20, f'{data_json[device]["rain24"]:5.1f} mm')

      yindex = yindex + 2
      stdscr.addstr(yindex, 0, 'Battery Levels')
      for device in data_json:
        if 'battery' in data_json[device]:
          yindex += 1
          stdscr.addstr(yindex, 2, f'{device}: ')
          stdscr.addstr(yindex, 23, f'{data_json[device]["battery"]: 3d} %')

      stdscr.refresh()

      time.sleep(UPDATE_INTERVAL * 60)
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
    output[get_module_name(module)] = get_module_data(module, timezone)

  return output


def get_module_name(module_data):
  return module_data['module_name']

def get_module_data(module_data, timezone):
  if module_data['type'] == 'NAMain':
    return get_main_data(module_data, timezone)
  elif module_data['type'] == 'NAModule1':
    return get_outdoor_data(module_data, timezone)
  elif module_data['type'] == 'NAModule4':
    return get_indoor_data(module_data, timezone)
  elif module_data['type'] == 'NAModule3':
    return get_rain_data(module_data, timezone)

def get_main_data(module_data, timezone):
  result = {}
  result['time'] = str(get_date(module_data, timezone))
  result['temperature'] = get_value(module_data, 'Temperature')
  result['humidity'] = get_value(module_data, 'Humidity')
  result['pressure'] = get_value(module_data, 'Pressure')
  result['co2'] = get_value(module_data, 'CO2')
  return result

def get_outdoor_data(module_data, timezone):
  result = {}
  result['time'] = str(get_date(module_data, timezone))
  result['battery'] = get_battery(module_data)
  result['temperature'] = get_value(module_data, 'Temperature')
  result['humidity'] = get_value(module_data, 'Humidity')
  return result

def get_indoor_data(module_data, timezone):
  result = {}
  result['time'] = str(get_date(module_data, timezone))
  result['battery'] = get_battery(module_data)
  result['temperature'] = get_value(module_data, 'Temperature')
  result['humidity'] = get_value(module_data, 'Humidity')
  result['co2'] = get_value(module_data, 'CO2')
  return result

def get_rain_data(module_data, timezone):
  result = {}
  result['time'] = str(get_date(module_data, timezone))
  result['battery'] = get_battery(module_data)
  result['rain24'] = get_value(module_data, 'sum_rain_24')
  return result

def get_date(module_data, timezone):
  utc = module_data['dashboard_data']['time_utc']
  return datetime.fromtimestamp(utc, tz=timezone)

def get_battery(module_data):
  return module_data['battery_percent']

def get_value(module_data, item):
  try:
    return module_data['dashboard_data'][item]
  except Exception:
    println(module_data)
    global ERROR
    ERROR = traceback.format_exc()

curses.wrapper(main)
if ERROR is not None:
  print(f'{ERROR}')
