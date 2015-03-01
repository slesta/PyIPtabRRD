lan = 'eth1'
#lan = 'wlan0'
wan = 'eth0'
trafic = 'True'
wwwpath = '/var/www/html/pyiptabrrd/'
wwwhead = '<html><head><title>PyIptabRRD</title></head><body><table><tr><td>LAN - download</td><td>WAN - upload</td></tr>'
wwwfooter = '</table></body></html>'
iptrafgrafs = [
    '192.168.222.2',
    '192.168.222.10',
    '192.168.222.11',
    '192.168.222.12',
    '192.168.222.13',
]
iptrafgrafsud = [
    ['192.168.222.10', '192.168.223.1'],
    ['192.168.222.10', '192.168.223.3'],
    ['192.168.222.10', '192.168.223.4'],
    ['192.168.222.13', '192.168.223.1'],
    ['192.168.222.13', '192.168.223.3'],
    ['192.168.222.13', '192.168.223.4'],

]