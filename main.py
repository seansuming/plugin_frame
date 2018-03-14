# -- coding: utf-8 --
__author__ = 'Sean'


import sys
from manager import plugin_manager


if __name__ == '__main__':
    #加载所有
    plugin_manager.PluginManager.LoadAllPlugin()

    #遍历所有接入点下的所有插件
    for SingleModel in plugin_manager.__ALLMODEL__:
        plugins = SingleModel.GetPluginObject()
        for item in plugins:
            item.set_param('2018-03-14','2018-03-14',['600295','600123'])
            #调用接入点的公共接口
            item.start()
