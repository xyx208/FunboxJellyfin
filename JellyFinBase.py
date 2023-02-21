# -*- coding: utf-8 -*-
import requests
import re

host = 'https://192.168.1.22:8098/'#jellyfin地址
user_id = 'XXXXXXXXXXXXXXXXXXXXXX' #jellyfin user_id
api_key = 'XXXXXXXXXXXXXXXXXXXXXX' #jellyfin api_key


def isKey(_key, list):
    """
        :param _key: 关键字
        :param list: 比对列表
        """
    for x in list:
        if (_key.lower() == x.lower() or
                (_key.lower().replace('_', '-') == x.lower() and _key.split('_')[-1] not in ['01', '001']))\
                and all(c in "0123456789_-" for c in x):
            return x
    return None


def searchIfExistsInServer(_key, _type=None, _year=None):
    """
    :param _key: 输入查询文本
    :param _type: 查询类型：Movie,Series,Episode....
    :param _year:限定查询年份
    :return:res_items
    """
    _typestr = ""
    res_items = ['']
    if _type is not None:
        _typestr = "&IncludeItemTypes=%s" % _type
    url_dest = "%sUsers/%s/Items?api_key=%s&searchTerm=%s%s&Limit=10&Recursive=true" % (
        host, user_id, api_key, _key, _typestr)
    # print(url_dest)
    res = requests.get(url_dest, timeout=20)
    if res:
        res_items = res.json().get("Items")
        for item in res_items:
            # print(_key.replace('_', '-'))
            # print(str(item.get('Name')))
            if (_key.split('_')[-1] in ['01', '001'] or _key.split('-')[-1] in ['01', '001']) and str(item.get('IsFolder')) != 'True':
                if _key in str(item.get('Name')):#and isKey(_key, item.get('Name').split(' ')) is not None:
                   return item
            elif (_key.lower() in str(item.get('Name')).lower() or _key.lower().replace('_', '-') in str(item.get('Name')).lower()) and str(item.get('IsFolder')) != 'True':
                return item



if __name__ == '__main__':
    print(searchIfExistsInServer('121511_220'))
