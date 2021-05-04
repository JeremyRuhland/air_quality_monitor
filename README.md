Indoor Air Monitor
==================

The following details my indoor air quality monitoring setup.

Purchased an [Awair Element](https://www.getawair.com/home/element) sensor and [enabled the local API](https://support.getawair.com/hc/en-us/articles/360049221014-Awair-Local-API-Feature).

Signed up for a free api key on [OpenWeatherMap](https://openweathermap.org/) to receive outdoor conditions for my city.

Installed the following on a server on my LAN:

* [Grafana](https://grafana.com/)
* [InfluxDB](https://www.influxdata.com)
* [InfluxDB-Python](https://github.com/influxdata/influxdb-python)

Created a database in InfluxDB called "indoor_air_quality".

Created a dashboard in grafana, stored in air_quality_monitor_grafana_dashboard.json

Installed the two python scripts, gave them execute permissions and modified both for my personal API keys and awair serial number:

* awair_air_quality_monitor.py
* owm_weather.py

Installed local user systemd services to periodically run the scripts, enabled and started all of them:

* awair_air_quality_monitor.service
* awair_air_quality_monitor.timer
* owm_weather.service
* owm_weather.timer

![Dashboard](https://raw.githubusercontent.com/JeremyRuhland/air_quality_monitor/dashboard.jpg)
