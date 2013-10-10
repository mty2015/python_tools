# encoding: utf-8

"""
Translate string of html to obj by specified regular
"""

import re
import HTMLParser


class HtmlParser():
    def __init__(self, regular):
        self.regular = regular

    def parse(self, html):
        return parseNode(self.regular, html)


def processReg(exp, html, group_index=1):
    p = re.compile(exp, re.DOTALL)
    m = p.search(html)
    if m:
        try:
            return tripHtmlCode(m.group(group_index)).strip()
        except IndexError:
            pass


h = HTMLParser.HTMLParser()
u = h.unescape
space_tag = {r'\t': ' ',
             r'\r\n': ' '}


def tripHtmlCode(html):
    if not html:
        return ''
        #substitute the html tag    (?s)指定.匹配模式
    html = re.sub(r'(?s)<.+?>', '', html)
    #unenscape the html
    html = u(html)
    #替换多余的空格，包括中间出现的空格（空格包括space,tab,\r,\n,\r\n等空白字符）
    html = re.sub(r'\s+', ' ', html)
    html = html.replace(u'\xa0', u'')
    return html


def replaceHtmlTag(match):
    return match.group(1)


def parseNode(node, html):
    if type(node) is list:
        objList = []
        for itemStr in getSubHtmlGenerator(node[0], html):
            objList.append(parseNode(node[1], itemStr))
        return objList
    else:
        obj = {}
        for name, regular in node.items():
            if type(regular) is str or type(regular) is unicode:
                if name == "field_group_reg":  # field_group_reg为组件关键字，是对字典型对象字段的统一正则表达式，只是分组不同
                    continue
                obj[name] = processReg(regular, html)
            elif type(regular) is int:
                obj[name] = processReg(node['field_group_reg'], html, regular)
            else:
                obj[name] = parseNode(regular, html)
        return obj


def getSubHtmlGenerator(listConfig, html):
    groupKey = listConfig['groupKey']
    if 'startKey' in listConfig:
        startKey = listConfig['startKey']
        startPos = html.find(startKey)
        if startPos != -1:
            html = html[startPos + len(startKey):]
    if 'endKey' in listConfig:
        endKey = listConfig['endKey']
        endPos = html.find(endKey)
        if endPos != -1:
            html = html[:endPos]

    while True:
        start = html.find(groupKey)
        if start != -1:
            end = html[start + len(groupKey):].find(groupKey)
            if end != -1:
                yield html[start:end + start + len(groupKey)]
                html = html[end + start + len(groupKey):]
            else:
                yield html[start:]
                break
        else:
            break