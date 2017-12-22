#!/bin/sh
# Get hostname
hostname=`hostname ` 2> /dev/null

# Get distro
#distro=$(awk -F= 'END { print $2 }' /etc/lsb-release)
#distro=`echo $distro | sed 's/^.\(.*\).$/\1/'`
# Get uptime
if [ -f "/proc/uptime" ]; then
uptime=`cat /proc/uptime`
uptime=${uptime%%.*}
seconds=$(( uptime%60 ))
minutes=$(( uptime/60%60 ))
hours=$(( uptime/60/60%24 ))
days=$(( uptime/60/60/24 ))
#uptime="$days days, $hours hours, $minutes minutes, $seconds seconds"
uptime="$days/$hours:$minutes:$seconds"
else
uptime=""
fi

#printf '{"hostname":"%s","distro":"%s","uptime":"%s"}\n' "$hostname" "$distro" "$uptime"
printf "$USER@$hostname çalışma zamanı:$uptime"
