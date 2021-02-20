import requests
import toml
import netatmo
import json
from datetime import datetime
import pytz

def main(config):
  weather_data = get_data(config['netatmo'])
  data_output = build_output(weather_data)

  with open('weather.json', 'w') as f:
    json.dump(data_output, f)



def get_data(account_config):
  ws = netatmo.WeatherStation(account_config)
  ws.get_data()
  return ws.devices

def build_output(data):
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
  return module_data['dashboard_data'][item]

if __name__ == '__main__':
  config = toml.load('config.toml')
  main(config)
