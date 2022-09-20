# yubihsm

## Startup Scripts

### :green_circle: On demand startup
These scripts require some pre-configuration before they can be used. The .config file needs to have
information updated with the YubiHSM details.

#### Files

- hsm_list.config
- startup_hsm.sh


### :yellow_circle: On Insert configuration :construction: 

These scripts are intended to auto config the YubiHSM connector service when a new YubiHSM is inserted.

:rotating_light: NOTE: You may have some security exposure using these script. Not intended to be run in untrusted environment.

#### Files

- hsminsert.sh
- yubihsm.rules
