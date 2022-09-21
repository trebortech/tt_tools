# yubihsm

## Startup Scripts

### Status :green_circle: for "On demand startup"
These scripts require some pre-configuration before they can be used. The .config file needs to have
information updated with the YubiHSM details.

#### Files

- hsm_list.config
- startup_hsm.sh


### Status :green_circle: fir "On Insert configuration"

These scripts are intended to auto config the YubiHSM connector service when a new YubiHSM is inserted.

:rotating_light: NOTE: You may have some security exposure using these script. Not intended to be run in untrusted environment.

#### Files

- /usr/loca/bin/hsminsert.sh  <-- chmod +x
- /etc/udev/rules.d/yubihsm.rules
- /etc/systemd/system/yubihsm-start.service   <-- chmod +x

Reload systemd
```bash
systemctl daemon-reload
```

Reload udev rules
```bash
udevadm control --reload
```