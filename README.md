# Mikrotik RESTful API

Early build of a simple Mikrotik API connector for the RouterOS v7 API.

Mikrotik REST API Documentation is available in the [official docs](https://help.mikrotik.com/docs/display/ROS/REST+API)

## TODO:
☑ Initial commit\
Exception handling\
Actual documentation\
Initial PyPI upload

## The ID value:
The ID requested by Set and Remove can be obtained by either a get or search.\
Output from get interface/vlan:\
```
{'.id': '*37', 'arp': 'enabled', 'arp-timeout': 'auto', 'disabled': 'false', 'interface': 'zerotier1', 'loop-protect': 'default', 'loop-protect-disable-time': '5m', 'loop-protect-send-interval': '5s', 'loop-protect-status': 'off', 'mac-address': 'C0:FF:EE:C0:FF:EE', 'mtu': '1500', 'name': 'vlanexample', 'running': 'true', 'use-service-tag': 'false', 'vlan-id': '123'}
```
The ID to use for Set and Remove on this vlan is "*37"