# -- coding: utf-8 --
__author__ = 'Sean'



from manager.plugin_manager import ModelStockTest
from manager.plugin_manager import ModelStockSimple
import tushare as ts
from utils.stock import StockUtil
from datetime import datetime
from pandas import DataFrame
import numpy
import time

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class PluginStockTest(ModelStockTest):
    def __init__(self):
        self._time_start = ''
        self._time_end = ''
        self._codes = ''

    def set_param(self, time_start, time_end, codes):
        d=ts.get_stock_basics()
        self._time_start = time_start
        self._time_end = time_end
        d=ts.get_stock_basics()
        self._codes = d.index

    # 实现接入点的接口
    def start(self):

        days = StockUtil().get_date_list(datetime.strptime(self._time_start, '%Y-%m-%d'),
                                         datetime.strptime(self._time_end, '%Y-%m-%d'))
        matchtotal=0
        uptotal=0
        j=0
        for code in self._codes:
            j+=1
            print ('%d/%d current=%s' %(j,len(self._codes),code))
            for i in range(len(days)-1):
                ds = ts.get_sina_dd(code=code, date=days[i],vol=400)
                # ds['total']=ds.price*ds.volume
                # maipantol=ds[ds.type=='买盘'].total.sum()
                # maipan1tol=ds[ds.type=='卖盘'].total.sum()
                if ds is None:
                    continue
                maipantol=ds[ds.type=='买盘'].volume.sum()
                maipan1tol=ds[ds.type=='卖盘'].volume.sum()
                jinliuru=maipantol-maipan1tol

                df= ts.get_hist_data(code=code,start=days[i],end=days[i+1])
                # keys=numpy.array(df.volume.keys).tolist()
                # if not days[i] in keys:
                #     continue
                if days[i] not in df.volume:
                    continue

                chengjiaoliang=df.volume[days[i]]
                liuruzhanbi=jinliuru/100/chengjiaoliang
                if days[i] not in df.close:
                    continue
                dangtianshoupan=df.close[days[i]]
                if liuruzhanbi<0.30:
                    continue
                if days[i+1] not in df.high:
                    continue
                matchtotal+=1
                secdayhigh=df.high[days[i+1]]
                secdayzhangfu=(secdayhigh-dangtianshoupan)/dangtianshoupan
                if secdayzhangfu>0.0:
                    uptotal+=1
                    print ('date=%s,code=%s,zhangfu=%s,a=%s,b=%s,c=%s' %(str(days[i]),str(code),str(secdayzhangfu),str(secdayhigh),str(dangtianshoupan),str(liuruzhanbi)))
                # print ('date=%s,code=%s,zhangfu=%s,jinliuru=%s' %(str(days[i]),str(self._codes[0]),str(secdayzhangfu),str(jinliuru)))
        print ('total=%d,match=%d' %(matchtotal,uptotal))

            # for code in self._codes:
            #     print code


class PluginStockSimple(ModelStockSimple):
    def __init__(self):
        pass

    def set_param(self, time_start, time_end, codes):
        d=ts.get_stock_basics()
        self._time_start = time_start
        self._time_end = time_end
        d=ts.get_stock_basics()
        self._codes = d.index

    def start(self):
        matchs=[]
        j=0
        for code in self._codes:
            if code.startswith('300'):
                continue
            j+=1
            print ('%d/%d current=%s' %(j,len(self._codes),code))
            ds = ts.get_sina_dd(code=code, date=self._time_start,vol=400)
                # ds['total']=ds.price*ds.volume
                # maipantol=ds[ds.type=='买盘'].total.sum()
                # maipan1tol=ds[ds.type=='卖盘'].total.sum()
            if ds is None:
                continue
            maipantol=ds[ds.type=='买盘'].volume.sum()
            maipan1tol=ds[ds.type=='卖盘'].volume.sum()
            jinliuru=maipantol-maipan1tol

            # df= ts.get_hist_data(code=code,start=self._time_start,end=self._time_start)
            time.sleep(1)
            df=ts.get_realtime_quotes(code)
                # keys=numpy.array(df.volume.keys).tolist()
                # if not days[i] in keys:
                #     continue
            if 0 not in df.volume:
                continue

            chengjiaoliang=float(df.volume[0])
            if jinliuru==0.0 or chengjiaoliang==0.0:
                continue
            liuruzhanbi=jinliuru/chengjiaoliang

            # p_change=(df.price-df.open[0])/df.open[0]
            if liuruzhanbi<0.30:
                print liuruzhanbi
                continue

            matchs.append(code)
            print ('date=%s,code=%s,liuruzhanbi=%s' %(str(self._time_start),str(code),str(liuruzhanbi)))
                # print ('date=%s,code=%s,zhangfu=%s,jinliuru=%s' %(str(days[i]),str(self._codes[0]),str(secdayzhangfu),str(jinliuru)))
        print matchs

            # for code in self._codes:
            #     print code
