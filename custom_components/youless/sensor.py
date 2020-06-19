"""
@ Author      : Rutger Koebrugge, Gerben Jongerius, Paul de Wit, Robin Harmsen
@ Date        : 04/13/2020, 04/29/2018, 11/01/2018, 04/29/2019
@ Description : Youless Sensor - Monitor power consumption. This component will add the following sensors
                   - Current power consumption (in W)
                   - Current tick count, since the Youless meter started running (in kWh)
                This version (2.0.2) is a fork to support the older YouLess LS110.
"""
VERSION = '2.0.5'

import json
import logging
import time
from datetime import timedelta
from urllib.request import urlopen

import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_MONITORED_VARIABLES
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle

DOMAIN = 'youless'
CONF_HOST = "host"
CONF_MONITORED_VARIABLES = "monitored_variables"

SENSOR_PREFIX = 'youless_'
_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_HOST): cv.string,
        vol.Optional(CONF_MONITORED_VARIABLES, default=['pwr', 'cnt']): vol.All(
            cv.ensure_list, vol.Length(min=1), [vol.In(['pwr', 'cnt'])])
    })
}, extra=vol.ALLOW_EXTRA)

SENSOR_TYPES = {
    'pwr': ['Current Power usage', 'current_power_usage', 'W', 'mdi:flash'],
    'cnt': ['Net Power usage', 'net_power_meter', 'kWh', 'mdi:gauge']
}


def setup_platform(hass, config, add_devices, discovery_info=None):
    host = config.get(CONF_HOST)
    sensors = config.get(CONF_MONITORED_VARIABLES)
    data_bridge = YoulessDataBridge(host)

    devices = []
    for sensor in sensors:
        sensor_config = SENSOR_TYPES[sensor]
        devices.append(YoulessSensor(data_bridge, sensor_config[0], sensor, sensor_config[1], sensor_config[2], sensor_config[3]))

    add_devices(devices)


class YoulessDataBridge(object):

    def __init__(self, host):
        self._url = 'http://' + host + '/a?f=j'
        self._data = None

    def data(self):
        return self._data

    @Throttle(timedelta(seconds=1))
    def update(self):
        raw_res = urlopen(self._url)
        self._data = json.loads(raw_res.read().decode('utf-8'))


class YoulessSensor(Entity):

    def __init__(self, data_bridge, name, prpt, sensor_id, uom, icon):
        self._state = None
        self._name = name
        self._property = prpt
        self._icon = icon
        self._uom = uom
        self._data_bridge = data_bridge
        self.entity_id = 'sensor.' + SENSOR_PREFIX + sensor_id
        self._raw = None

    @property
    def name(self):
        return self._name

    @property
    def icon(self):
        return self._icon

    @property
    def unit_of_measurement(self):
        return self._uom

    @property
    def state(self):
        return self._state

    @property
    def state_attributes(self):
        if self._raw is not None:
            return {
                'timestamp': int(time.time())
            }

    def update(self):
        self._data_bridge.update()
        self._raw = self._data_bridge.data()
        if self._raw is not None:
            if type(self._raw[self._property]) == str:
                self._raw[self._property] = float(self._raw[self._property].replace(',', '.'))
            
            self._state = self._raw[self._property]
