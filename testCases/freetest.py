# coding: utf-8

import re

s = u'中\大包装:100 \ 100'

res = s.split(':')[1].split('\\')[1].split(' ')[1]
print res

