#!/usr/bin/python

import re
class store:
    incremt = 22
    items = 0
    def __init__ (self, item1,item2,place,costt):
        self.item1 = item1
        self.item2 = item2
        self.item3 = item1+ " "+item2+ " "+place
        self.costt = costt
        store.items += 1
