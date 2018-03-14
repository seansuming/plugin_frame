# -- coding: utf-8 --
__author__ = 'Sean'

from datetime import datetime
from datetime import timedelta


class StockUtil(object):
    def compute_jinge(self, data):
        pass

    def compute_zhanbi_dadan(self, data):
        pass

    def compute_zhanbi_judan(self, data):
        pass

    def compute_zhanbi_jinge(self, data):
        pass

    def compute_zhangfu(self, lishijia, dangqianjia):
        pass

    def is_work_day(self, d):
        weekday_int = d.weekday()
        return weekday_int <= 4 and weekday_int >= 0

    def get_date_list(self,start=None, end=None):
        """
        获取日期列表
        :param start: 开始日期
        :param end: 结束日期
        :return:
        """
        data = []
        if start is None:
            return data
        if end is None:
            return data
        for d in self.__gen_dates(start, (end-start).days):
            if self.is_work_day(d):
                data.append(datetime.strftime(d, "%Y-%m-%d"))
        return data

    def __gen_dates(self,b_date, days):
        day = timedelta(days=1)
        for i in range(days):
            yield b_date + day*i