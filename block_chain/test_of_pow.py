#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
工作量证明算法

Created by C.L.Wang
"""

from block_chain.blockchain import Blockchain

x = 5
y = 0  # y未知
while Blockchain.hash(x * y)[-1] != "0":
    y += 1
print "Hash: %s" % Blockchain.hash(x * y)
print('The solution is y = {y}'.format(y=y))

bc = Blockchain()
print "新的工作量: %s" % bc.proof_of_work(100)
