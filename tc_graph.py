#!/usr/bin/env python
# -*- coding: utf-8 -*-


import time
import os
from tcvars import *
import datetime

from pyrrd.rrd import RRD, RRA, DS
from pyrrd.graph import DEF, CDEF, VDEF
from pyrrd.graph import LINE, AREA, GPRINT, PRINT, COMMENT
from pyrrd.graph import ColorAttributes, Graph


def Tcgraph():
    exampleNum = 1

    min = 60
    hour = 60 * 60
    day = 24 * 60 * 60
    week = 7 * day
    month = day * 30
    quarter = month * 3
    half = 365 * day / 2
    year = 365 * day
    now = int(time.time())

    endTime = now
    startTime = str(now - 600)
    zacalo = datetime.datetime.today()


    #### index pro web
    filenam = wwwpath + 'index.html'
    soubor = file(filenam, 'w')
    soubor.write(wwwhead)

    adr_list = os.listdir('rrd/')
    for adr in adr_list:


        filename = 'rrd/%s' % adr
        print filename
        graphfile = wwwpath + '%s.png' % adr.replace('.rrd', '')
        graphfile_lg = 'graphs/%s.png' % adr.replace('.rrd', '')
        hgraphfile_lg = wwwpath + '%sh.png' % adr.replace('.rrd', '')
        dgraphfile_lg = 'graphs/%sd.png' % adr.replace('.rrd', '')
        wgraphfile_lg = 'graphs/%sw.png' % adr.replace('.rrd', '')
        mgraphfile_lg = 'graphs/%sm.png' % adr.replace('.rrd', '')
        ygraphfile_lg = 'graphs/%sy.png' % adr.replace('.rrd', '')
        now = int(time.time())
        endTime = now
        startTime = str(now - 600)
        myRRD = RRD(filename)

        def1 = DEF(rrdfile=myRRD.filename, vname='dsnameupall', dsName='upall')
        def2 = DEF(rrdfile=myRRD.filename, vname='dsnamedownall', dsName='downall')


        #cdef2 = CDEF(vname='mybitstx', rpn='%s,-8,*' % def2.vname)
        cdef1 = CDEF(vname='sdsnameupall', rpn='%s,8,*' % def1.vname)
        cdef2 = CDEF(vname='sdsnamedownall', rpn='%s,-8,*' % def2.vname)
        #vdef1 = VDEF(vname='myavgrx', rpn='%s,AVERAGE' % cdef1.vname)

        #area2 = AREA(defObj=cdef2, color='#468A41', legend='Up rate', width='2')
        area1 = AREA(defObj=cdef1, color='#8399f770', legend='upload', width='1')
        area2 = AREA(defObj=cdef2, color='#468A4170', legend='download', width='1')
        area3 = LINE(defObj=cdef1, color='#8399f7', legend='', width='1')
        area4 = LINE(defObj=cdef2, color='#468A41', legend='', width='1')


        vdef1 = VDEF(vname='myavgrx', rpn='%s,TOTAL' % def2.vname)
        vdef2 = VDEF(vname='myavgtx', rpn='%s,TOTAL' % def1.vname)
        gprint1 = GPRINT(vdef1, 'downloaded %lf %sbytes')
        gprint2 = GPRINT(vdef2, 'uploaded %lf %sbytes')

        comment1 = COMMENT('textik')

        ca = ColorAttributes()
        ca.back = '#333333'

        ca.canvas = '#333333'

        ca.shadea = '#000000'
        ca.shadeb = '#111111'
        ca.mgrid = '#CCCCCC'
        ca.axis = '#FFFFFF'
        ca.frame = '#AAAAAA'
        ca.font = '#FFFFFF'
        ca.arrow = '#FFFFFF'

        nadpis = adr + ' - ' + str(datetime.datetime.today())
        graphwidth = 600
        graphheight = 200

        print hgraphfile_lg

        gh = Graph(hgraphfile_lg, start=int(time.time()) - min*20, end=endTime, vertical_label='bits/s', color=ca)
        gh.width = graphwidth

        gh.height = graphheight
        text = nadpis
        text = text.replace(' ', '_')
        gh.title = text
        gh.data.extend([
                       def1, def2,
                       cdef1, cdef2,
                       area1, area2, area3, area4,
                       # area6, area10, area7, area8, area9,
                       vdef1, gprint1, vdef2, gprint2,
        ])

        gh.write()

        soubor.write('<td><img src="' + str(hgraphfile_lg).replace(wwwpath, '') + '"></td><td><img src="' + str(
                hgraphfile_lg).replace(wwwpath, '').replace('lan', 'wan') + '"></td></tr>')

    soubor.write(wwwfooter)
    soubor.close()

    dobabehu = datetime.datetime.today() - zacalo
    dobabehu = dobabehu.seconds
    print 'Doba zpracování grafů: ' + str(dobabehu) + ' sec.'


Tcgraph()