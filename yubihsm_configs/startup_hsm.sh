#!/bin/bash
configfile='./hsm_list.config'
. $configfile
hsmcount=$(grep -c 'serial' $configfile)
for (( c=1; c<=$hsmcount; c++))
    do
        hsmserial="hsm${c}_serial"
        hsmlisten="hsm${c}_listen"
        $connector_path --listen ${!hsmlisten} --serial ${!hsmserial} &
    done