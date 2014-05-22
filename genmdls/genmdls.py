# encoding: utf-8

"""
在已有的md文件上生成目录，方便阅读跳转
"""

import os, sys, re

# 标题模式
title_pattern = re.compile(r'^(#+)\s+(.*)')


def generateList(filePath):
    if not os.path.exists(filePath):
        print 'file not exists: {}'.format(filePath)
        sys.exit(1)

    if os.path.isfile(filePath) and filePath.endswith('.md'):
        bakPath =  filePath+'.bak'
        os.rename(filePath, bakPath)
        with open(bakPath, 'r') as bakFile:
            with open(filePath, 'w') as newFile:

                preTitleLevel = None
                spaceCount = 0
                listContent = ''

                for titleLine in bakFile:
                    if not title_pattern.match(titleLine):
                        continue
                    titleLevel, titleContent = title_pattern.search(titleLine).groups()
                    titleLevel = len(titleLevel)
                    if preTitleLevel:
                        if titleLevel > preTitleLevel:
                            spaceCount += 1
                        elif titleLevel < preTitleLevel:
                            spaceCount = spaceCount - (preTitleLevel - titleLevel)
                            if spaceCount < 0: spaceCount = 0

                    preTitleLevel = titleLevel

                    listContent += (' '*(spaceCount*4) + '1. ' + titleContent + '\n')

                # 在头部写入目录
                newFile.write(listContent + '\n')
                # 重置
                bakFile.seek(0)

                for contentLine in bakFile:
                    newFile.write(contentLine)

        os.remove(bakPath)







if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'usage: genmdls.py filePath'
        sys.exit(1)
    generateList(sys.argv[1])