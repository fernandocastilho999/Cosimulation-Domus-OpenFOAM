#!/bin/bash

#Time control
start_time=$(date +%s)

# Power on the VM
vbon=$(vboxmanage showvminfo "win10b" | grep -c "running (since")

if [ $vbon -eq 1 ]; then
    echo "The VM is ON"
else
    # echo "Turning on VM"
    VBoxManage startvm "win10b"
    # sleep 45s #PowerOn

    # sleep 15s # PowerOff
    # echo "VM TurnedOn"

    vblogon=0
    while [ $vblogon -eq 0 ]; do
        # echo $vblogon
        sleep 1s
        vblogon=$(vboxmanage showvminfo "win10b" | grep -c "VirtualBox System Service")
    done
    # sleep 5s
fi

# Copy IDf file
reslocal='../domus/'
dirshare='/media/hdd3/vboxFiles/pucpr/research/energy/domus/ap04/'
dirwin='C:\Users\fernando\Documents\workspace\phd\domus\'

cn="box_exported_conf"
fn=$cn".idf"
VBoxManage guestcontrol "win10b" copyto $dirshare$fn $dirwin$fn
ln -sf $dirshare$fn $reslocal$fn

# Remnove Old simulation directoy
simdir=$dirwin"#"$cn
echo $simdir
VBoxManage guestcontrol "win10b" rmdir -R $simdir

# Runcase with a bat file
domcon='"C:\Program Files (x86)\Domus - Eletrobras\Win32\Release\DomusConsole.exe"'
runcase=$domcon" -q -txt "$dirwin$fn
echo $runcase >/tmp/runcase.bat
VBoxManage guestcontrol "win10b" copyto "/tmp/runcase.bat" $dirwin"\runcase.bat"
vboxmanage guestcontrol "win10b" run --exe $dirwin"\runcase.bat"

# Copy files to workspace
# sleep 5s
resdirwin="$simdir\saidas\sim001"

rm -rf $reslocal/sim001
VBoxManage guestcontrol "win10b" copyfrom -R --target-directory $reslocal $resdirwin

rm -rf $reslocal/sim001/*.sda

# vboxmanage controlvm "win10b" acpipowerbutton

# measure time
end_time=$(date +%s)
# elapsed time with second resolution
elapsed=$((end_time - start_time))
echo $elapsed" seconds"
