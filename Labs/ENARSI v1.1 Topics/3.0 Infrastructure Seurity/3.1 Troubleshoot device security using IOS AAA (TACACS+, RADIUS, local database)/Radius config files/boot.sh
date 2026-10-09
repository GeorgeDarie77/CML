# insert more commands here
ip address add dev eth0 192.168.2.254/24
ip link set dev eth0 up
ip route add default via 192.168.2.1 dev eth0
#
# keep the next line to indicate that the machine is ready
echo "READY" >/dev/console
exit 0