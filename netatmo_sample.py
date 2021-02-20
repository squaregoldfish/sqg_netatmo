# Example dict returned from ws.devices
{
  [
    {
      "_id": "00:00:00:00:00:00",
      "station_name": "Home",
      "date_setup": 1457790071,
      "last_setup": 1457790071,
      "type": "NAMain",
      "last_status_store": 1613820066,
      "module_name": "Kitchen",
      "firmware": 177,
      "last_upgrade": 1498344043,
      "wifi_status": 57,
      "reachable": True,
      "co2_calibrating": False,
      "data_type": ["Temperature", "CO2", "Humidity", "Noise", "Pressure"],
      "place": {
        "altitude": 69,
        "city": "Haugo",
        "country": "NO",
        "timezone": "Europe/Oslo",
        "location": [0.0, 0.0]
      },
      "home_id": "aaaaaaaaaaaaaaaaa",
      "home_name": "Home",
      "dashboard_data": {
        "time_utc": 1613820048,
        "Temperature": 17.7,
        "CO2": 522,
        "Humidity": 47,
        "Noise": 40,
        "Pressure": 1003.3,
        "AbsolutePressure": 995.2,
        "min_temp": 16.7,
        "max_temp": 18.2,
        "date_max_temp": 1613804329,
        "date_min_temp": 1613796474,
        "temp_trend": "stable",
        "pressure_trend": "up"
      },
      "modules": [
        {
          "_id": "00:00:00:00:00:00",
          "type": "NAModule1",
          "module_name":"Outdoor module",
          "last_setup": 1457790089,
          "data_type": ["Temperature", "Humidity"],
          "battery_percent": 62,
          "reachable": True,
          "firmware": 50,
          "last_message": 1613820060,
          "last_seen": 1613820060,
          "rf_status": 71,
          "battery_vp": 5308,
          "dashboard_data": {
            "time_utc": 1613820009,
            "Temperature": 7.1,
            "Humidity": 96,
            "min_temp": 6.2,
            "max_temp": 7.1,
            "date_max_temp": 1613820009,
            "date_min_temp": 1613780736,
            "temp_trend": "up"
          }
        },
        {
          "_id": "00:00:00:00:00:00",
          "type": "NAModule4",
          "module_name": "Bedroom",
          "last_setup": 1500721688,
          "data_type": ["Temperature", "CO2", "Humidity"],
          "battery_percent": 85,
          "reachable": True,
          "firmware": 50,
          "last_message": 1613820060,
          "last_seen": 1613820022,
          "rf_status": 59,
          "battery_vp": 5732,
          "dashboard_data": {
            "time_utc": 1613820022,
            "Temperature": 19.4,
            "CO2": 544,
            "Humidity": 39,
            "min_temp": 19,
            "max_temp": 20,
            "date_max_temp": 1613804282,
            "date_min_temp": 1613797053,
            "temp_trend": "stable"
          }
        },
        {
          "_id": "00:00:00:00:00:00",
          "type": "NAModule3",
          "module_name": "Rain",
          "last_setup": 1601572158,
          "data_type": ["Rain"],
          "battery_percent": 89,
          "reachable": True,
          "firmware": 12,
          "last_message": 1613820060,
          "last_seen": 1613820060,
          "rf_status": 67,
          "battery_vp": 5748,
          "dashboard_data": {
            "time_utc": 1613820047,
            "Rain": 0,
            "sum_rain_1": 1.313,
            "sum_rain_24": 9.1
          }
        }
      ]
    }
  ]
}