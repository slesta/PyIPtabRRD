#!/usr/bin/env python
# -*- coding: utf-8 -*-


import datetime
import time
import os
import subprocess
import re

from pyrrd.rrd import RRD, RRA, DS
from pyrrd.graph import DEF, CDEF, VDEF
from pyrrd.graph import LINE, AREA, GPRINT
from pyrrd.graph import ColorAttributes, Graph

from tcvars import *


step = 2

min = 60
hour = 60 * 60
day = 24 * 60 * 60
week = 7 * day
month = day * 30
quarter = month * 3
half = 365 * day / 2
year = 365 * day

now = int(time.time())


def unitsconvert(value, unit):
    if unit == 'bit':
        return int(value)
    if unit == 'Kbit':
        return int(value) * 1000
    if unit == 'Mbit':
        return int(value) * 1000000
    if unit == 'Gbit':
        return int(value) * 1000000000


def createnetrules():
    filenamecr = 'createiptabacc.sh'
    if trafic:
        rows = []
        rows.append('#!/bin/sh')
        rows.append('echo 1')
        rows.append('/sbin/iptables -F TRAFFIC_ACC_IN')
        rows.append('echo 2')
        rows.append('/sbin/iptables -F TRAFFIC_ACC_OUT')
        rows.append('echo 3')
        rows.append('/sbin/iptables -D INPUT -i %s -j TRAFFIC_ACC_IN' % lan)
        rows.append('echo 4')
        rows.append('/sbin/iptables -D OUTPUT -o %s -j TRAFFIC_ACC_OUT' % lan)
        rows.append('echo 5')
        rows.append('/sbin/iptables -X TRAFFIC_ACC_IN')
        rows.append('echo 6')
        rows.append('/sbin/iptables -X TRAFFIC_ACC_OUT')
        rows.append('echo 7')
        rows.append('/sbin/iptables -N TRAFFIC_ACC_IN')
        rows.append('echo 8')
        rows.append('/sbin/iptables -N TRAFFIC_ACC_OUT')
        rows.append('echo 9')
        rows.append('/sbin/iptables -I INPUT -i %s -j TRAFFIC_ACC_IN' % lan)
        rows.append('echo 10')
        rows.append('/sbin/iptables -I OUTPUT -o %s -j TRAFFIC_ACC_OUT' % lan)
        rows.append('echo 11')
        rows.append('/sbin/iptables -Z TRAFFIC_ACC_IN')
        rows.append('echo 12')
        rows.append('/sbin/iptables -Z TRAFFIC_ACC_OUT')
        rows.append('echo 13')

        for iptrafgraf in iptrafgrafs:
            # print iptrafgraf.ip
            #rows.append('echo %s' % iptrafgraf.ip  )
            rows.append('/sbin/iptables -A TRAFFIC_ACC_IN --src %s' % iptrafgraf)
            rows.append('/sbin/iptables -A TRAFFIC_ACC_OUT --dst %s' % iptrafgraf)


    else:
        rows = []
        rows.append('#!/bin/sh')
        rows.append('/sbin/iptables -F TRAFFIC_ACC_IN')
        rows.append('/sbin/iptables -F TRAFFIC_ACC_OUT')
        rows.append('/sbin/iptables -X TRAFFIC_ACC_IN')
        rows.append('/sbin/iptables -X TRAFFIC_ACC_OUT')
    soubor = file(filenamecr, 'w')
    for row in rows:
        soubor.write(row)
        soubor.write('\n')
    soubor.close()


def feedrrd():
    uplist = []
    downlist = []
    #####################################  U P L O A D
    ####################################################################################################

    # iptables -L TRAFFIC_ACCT_OUT -n -v -x
    output = \
    subprocess.Popen(['iptables', '-L', 'TRAFFIC_ACC_OUT', '-n', '-v', '-x'], stdout=subprocess.PIPE).communicate()[0]
    # print output
    vystup = output[0:-1].split('\n')
    now = int(time.time())
    i = 0
    lastip = ''
    uplisti = []
    for line in vystup:
        rawifacenum = r"""(?P<pkt>([0-9]+))([ \t]+)(?P<bits>([0-9]+))([\t ]+)(?P<proto>([0-9a-zA-Z]+))([ \t -/*]+)(?P<src>([0-9/.]+))([ \t]+)(?P<dst>([0-9/.]+))((([ ]+$)|($))|([ \t]+)([ a-zA-Z:]+)(?P<port>([0-9]+)))"""
        r = re.compile(rawifacenum, re.U)
        #Prvni radek ip addr show
        pkt = ''
        bits = ''
        proto = ''
        src = ''
        dst = ''
        port = ''
        hjk = ''

        for prvek in r.finditer(line):
            pkt = prvek.group("pkt")
            bits = prvek.group("bits")
            proto = prvek.group("proto")
            src = prvek.group("src")
            dst = prvek.group("dst")
            if prvek.group("port"):
                port = prvek.group("port")
            else:
                port = ''
            uplisti = {'pkt': pkt, 'bits': bits, 'proto': proto, 'src': src, 'dst': dst, 'port': port, 'smer': 'up'}
            uplist.append(uplisti)
            i += i
            lastip = src

    ###################################### D O W N L O A D
    ##############################################################################################################


    output = \
    subprocess.Popen(['iptables', '-L', 'TRAFFIC_ACC_IN', '-n', '-v', '-x'], stdout=subprocess.PIPE).communicate()[0]
    #print output
    vystup = output[0:-1].split('\n')

    for line in vystup:
        rawifacenum = r"""(?P<pkt>([0-9]+))([ \t]+)(?P<bits>([0-9]+))([\t ]+)(?P<proto>([0-9a-zA-Z]+))([ \t -/*]+)(?P<src>([0-9/.]+))([ \t]+)(?P<dst>([0-9/.]+))((([ ]+$)|($))|([ \t]+)([ a-zA-Z:]+)(?P<port>([0-9]+)))"""
        r = re.compile(rawifacenum, re.U)
        #Prvni radek ip addr show
        pkt = ''
        bits = ''
        proto = ''
        src = ''
        dst = ''
        port = ''
        hjk = ''
        for prvek in r.finditer(line):
            pkt = prvek.group("pkt")
            bits = prvek.group("bits")
            proto = prvek.group("proto")
            src = prvek.group("src")
            dst = prvek.group("dst")
            if prvek.group("port"):
                port = prvek.group("port")
            else:
                port = ''
            downlisti = {'pkt': pkt, 'bits': bits, 'proto': proto, 'src': src, 'dst': dst, 'port': port, 'smer': 'down'}
            downlist.append(downlisti)
            i += i


    #print uplist
    #print downlist
    ##############  slouci upload a download
    bitsvalues = []
    rowbitsvalues = []
    lastip = ''
    i = 0
    for uprow in uplist:
        rowbitsvalues.append(uprow['bits'])
        lastip = uprow['src']
        #print uprow
        i = i + 1
        #print i
        if i == 1:
            #print 'je po up'
            for downrow in downlist:
                if downrow['dst'] == lastip:
                    rowbitsvalues.append(downrow['bits'])
            i = 0
            rowbitsvalues.append(lastip)
            bitsvalues.append(rowbitsvalues)
            rowbitsvalues = []

    #now=int(time.time())
    #print bitsvalues
    for bitsvalue in bitsvalues:
        print bitsvalue
        ip = bitsvalue[2].replace('.', '-')
        ip = ip.replace('/', '_')
        #print ip
        filename = 'rrd/%s.rrd' % ip
        #print filename
        if os.path.isfile(filename):
            #print filename
            myRRD = RRD(filename)
            #now=int(time.time())
            myRRD.bufferValue(now, bitsvalue[0], bitsvalue[1])
            myRRD.update()
        else:
            dss = []
            rras = []
            rezerva = 25
            ds1 = DS(dsName='upall', dsType='DERIVE', heartbeat=step + rezerva, minval=0)
            ds2 = DS(dsName='downall', dsType='DERIVE', heartbeat=step + rezerva, minval=0)
            dss.append(ds1)
            dss.append(ds2)

            rramin = RRA(cf='AVERAGE', xff=0.9, steps=1, rows=20 * 60)
            rras.append(rramin)

            #print step
            myRRD = RRD(filename, ds=dss, rra=rras, start=now, step=step)
            myRRD.create()


if trafic:
    createnetrules()
    subprocess.Popen(['chmod 777 createiptabacc.sh'], shell=True, stdout=subprocess.PIPE).communicate()[0]
    subprocess.Popen(['./createiptabacc.sh'], shell=True, stdout=subprocess.PIPE).communicate()[0]
    filenam = 'readiptabpid'
    soubor = file(filenam, 'w')
    soubor.write(str(os.getpid()))
    soubor.close()

    # print os.getpid()

    zabralo = step
    if not os.path.isdir('rrd'):
        subprocess.Popen(['mkdir rrd'], shell=True, stdout=subprocess.PIPE).communicate()[0]
    subprocess.Popen(['rm rrd/*'], shell=True, stdout=subprocess.PIPE).communicate()[0]
    while True:
        time.sleep(zabralo)
        start = datetime.datetime.today()
        feedrrd()
        zabralo = datetime.datetime.today() - start
        zabralo = (float(zabralo.microseconds) / 1000000)
        print str(zabralo) + ' sec.'
        zabralo = step - zabralo
        # if zabralo < step:
        # zabralo = step

