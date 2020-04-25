[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)  
# Custom YouLess LS110 Component for HomeAssistant
Home Assistant custom sensor for the (somewhat old) YouLess LS110

Based on the version of [Robin Harmsen](https://github.com/reharmsen/hass-youless-component) which was forked from [Gerben Jongerius](https://bitbucket.org/jongsoftdev/youless) and the aditions of pdwonline.

## Installation
1) create a folder called 'custom_components' if not exists into your Home Assistant configuration folder
2) create a folder called 'youless' in the custom_components folder. 
3) Download all files into this 'youless' folder

## Available sensors

 Sensor | Description | Measure
  --- | --- | --- 
  pwr | Current Power usage | W 
  net | Net Power usage | kWh 


## Configuration example

```yaml
  - platform: youless
    name: Youless
    host: <your youless IP address>
    monitored_variables:
      - pwr
      - net
```
