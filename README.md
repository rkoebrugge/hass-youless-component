[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/hacs/integration)  
# Custom YouLess LS110 Component for HomeAssistant
Home Assistant custom sensor for the YouLess LS110

Based on the version of [Robin Harmsen](https://github.com/reharmsen/hass-youless-component) which was forked from [Gerben Jongerius](https://bitbucket.org/jongsoftdev/youless) and the aditions of [pdwonline](https://github.com/pdwonline/youless).

## Installation
### HACS installation
1) Search in the Integration tab for 'Youless LS110' and click on the integration.
2) Click 'Install'
3) Proceed to add a sensor in your configuration.yaml, see example below

### Manual installation
1) Create a folder called 'custom_components' if not exists into your Home Assistant configuration folder
2) Create a folder called 'youless' in the custom_components folder. 
3) Download all files into this 'youless' folder
4) Proceed to add a sensor in your configuration.yaml, see example below

## Available sensors

 Sensor | Description | Measure
  --- | --- | --- 
  pwr | Current Power usage | W 
  cnt | Net Power usage | kWh 


## Configuration example

```yaml
sensor:
  - platform: youless
    host: <your youless IP address>
    monitored_variables:
      - pwr
      - cnt
```
