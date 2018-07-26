#!/bin/bash
# The following script keeps 12 backup older than 1 month, 4 backup between 1m and 1w
# Backup in one week is unlimited

cmd='rclone lsl gdrive:/rpi-sync'
cmd_del='rclone delete gdrive:/rpi-sync/'
list=`eval $cmd`
time_string='%Y-%m-%d'

current_date=`date +$time_string`
weekly_date=`date +$time_string -d'-7 day'`
monthly_date=`date +$time_string -d'-1 month'`

t_c=`date -d "$current_date" +%s`
t_w=`date -d "$weekly_date" +%s`
t_m=`date -d "$monthly_date" +%s`

ARR=($list) # split string

c_m=12      # num of backup kept older than 1 month
c_w=4       # num of backup kept for older than 1 week and newer than 1 month

ii=${#ARR[*]}
counter_m=0
counter_w=0
while ((ii>0))
do
    #echo $ii
    file_date=${ARR[$ii - 3]}
    t_d=`date -d "$file_date" +%s`
    #echo $file_date
    if [ $t_d -le $t_w ] 
    then                # file older than 1 week
        if [ $t_d -le $t_m ]  # and file older than 1 month
        then
            if [ $counter_m -gt $c_m ]
            then        # too many files older than 1 month
                #echo $cmd_del${ARR[$ii - 1]}
                eval $cmd_del${ARR[$ii - 1]} # assume a descent sequence, always delete files that are very old
            else
                let "counter_m++"
            fi
        else    # file older than 1week but fresher than 1 month
            if [ $counter_w -gt $c_w ]
            then        # too many shoots
                #echo $cmd_del${ARR[$ii - 1]}
                eval $cmd_del${ARR[$ii - 1]}
            else
                let "counter_w++"
            fi
        fi
    fi
    let "ii=ii-4"
done
#declare -p ARR 

# create new backup
tar -czvf /tmp/homepi-$current_date.tar.gz /home/pi/piscripts /home/pi/.bashrc /home/pi/.bash_profile /home/pi/.profile /home/pi/.vimrc /home/pi/.virtualenv /home/pi/sevenology
rclone sync -v /tmp/homepi-$current_date.tar.gz gdrive:/rpi-sync
