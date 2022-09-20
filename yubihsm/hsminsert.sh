#!/bin/bash

PORTFILE=/usr/local/bin/ports.conf
LISTENIP="0.0.0.0"
connector_path='/usr/bin/yubihsm-connector'


[[ -f "$PORTFILE" ]] || echo "11111" >> $PORTFILE
currprocess=$(ps -ef | grep 'yubihsm')
results=$(lsusb -d 1050:0030 -v 2>/dev/null | grep iSerial)

for OUTPUT in $results
do
        if [[ "$OUTPUT" =~ ^[0-9]{10}$ ]]; then
                cleanserial=$(echo $OUTPUT | sed 's/^0*//')
                if [[ "$currprocess" =~ "$cleanserial" ]]; then
                    echo "Process already running $cleanserial"
                else
                    # Lookup up ports file for previous port
                    currvalue=$(awk -v var=$cleanserial '$1 ~ var {print}' < $PORTFILE)
                    if [ -z "$currvalue" ]; then
                        # Get next port number from line 1
                        useport=$(sed '1!d' < $PORTFILE)
                        nextport=$((useport+10))
                        sed -i -r "1s/.*/$nextport/" $PORTFILE
                        echo "$cleanserial:$useport" >> $PORTFILE
                    else
                        useport=$(echo $currvalue | awk '{split($0,a,":"); print a[2]}')
                        # Startup with this port number
                    fi
                    # Start the process
                    ipport="$LISTENIP:$useport"
                    /usr/bin/noup $connector_path --listen $ipport --serial $cleanserial &
                fi
        fi
done