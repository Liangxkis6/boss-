from django.test import TestCase

list = range(1, 116)
cur_page = 10
nowList = []
visibleNumber = 10
min = cur_page - visibleNumber / 2
if min < 1:
    min = 1
max = cur_page + visibleNumber - 1
if max > list[-1]:
    max = list[-1]
print(min,max)

