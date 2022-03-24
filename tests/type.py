#! /usr/bin/env python

from typing import TypedDict


class Test(TypedDict):
    markets: list[str]

t = Test[ 'markets']

def tt(markets: Test['markets'] = ['coucou']):
    print(markets)
