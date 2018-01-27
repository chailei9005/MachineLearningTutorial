#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
区块链的算法演示

Created by C.L.Wang
"""
import hashlib
import json
import sys
from time import time
from urlparse import urlparse
from uuid import uuid4

import requests
from flask import jsonify, Flask, request

""" 区块的结构
block = {
    'index': 1,  # 索引
    'timestamp': 1506057125.900785,  # 时间戳
    'transactions': [  # 交易列表
        {
            'sender': "8527147fe1f5426f9dd545de4b27ee00",  # 发送者
            'recipient': "a77f5cdfa2934df3954a5c7c7da5df1f",  # 接收者
            'amount': 5,  # 交易数量
        }
    ],
    'proof': 324984774000,  # 工作量证明
    'previous_hash': "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"  # 前一个区块的Hash值
}
"""


class Blockchain(object):
    def __init__(self):
        self.chain = []  # 储存区块链
        self.current_transactions = []  # 存储交易链
        self.nodes = set()  # 存储节点信息
        self.new_block(proof=100, previous_hash=1)  # 创建创世块

    def new_block(self, proof, previous_hash=None):
        """
        创建新的区块, 并添加存储链中
        :param proof: <int> 通过工作证明算法(PoW, Proof of Work)获取的证明
        :param previous_hash: (Optional) <str> 块的前一个Hash值
        :return: <dict> 新块
        """
        block = {
            'index': len(self.chain) + 1,  # 块的索引
            'timestamp': time(),  # 时间
            'transactions': self.current_transactions,  # 当前的交易链
            'proof': proof,  # 工作量证明
            'previous_hash': previous_hash or self.hash(self.chain[-1]),  # 块的前一个Hash值
        }

        self.current_transactions = []  # 重置当前的交易链
        self.chain.append(block)  # 在交易链中添加块

        return block  # 返回创建的块

    def new_transaction(self, sender, recipient, amount):
        """
        生成新交易信息，信息将加入到下一个待挖的区块中
        :param sender: <str> 发送者的地址
        :param recipient: <str> 接受者的地址
        :param amount: <int> 数量
        :return: <int> 处理持有交易的块索引
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        """
        生成块的 SHA-256 hash值
        :param block: 区块
        :return: 区块的Hash值
        """
        block_string = json.dumps(block, sort_keys=True).encode()  # 字典需要排序, 保证Hash值的一致性
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        """
        获取链中的最后一个区块
        :return: 最后一个区块
        """
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        """
        简单的工作量证明:
         - 查找一个 p' 使得 hash(pp') 以4个0开头
         - p 是上一个块的证明,  p' 是当前的证明
        :param last_proof: <int>
        :return: <int>
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof  # 工作量值

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        验证证明: 是否hash(last_proof, proof)以4个0开头
        :param last_proof: <int> 上一次的工作量
        :param proof: <int> 当前的工作量
        :return: <bool> 工作量是否验证成功
        """
        guess = ('{last_proof}{proof}'.format(last_proof=last_proof, proof=proof)).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def register_node(self, address):
        """
        Add a new node to the list of nodes
        :param address: <str> Address of node. Eg. 'http://192.168.0.5:5000'
        :return: None
        """
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)  # 注册节点信息

    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid
        :param chain: <list> A blockchain
        :return: <bool> True if valid, False if not
        """
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print('{last_block}'.format(last_block=last_block))
            print('{block}'.format(block=block))
            print("\n-----------\n")
            # Check that the hash of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        """
        共识算法解决冲突
        使用网络中最长的链.
        :return: <bool> True 如果链被取代, 否则为False
        """

        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get('http://{node}/chain'.format(node=node))

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False


# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # 给工作量证明的节点提供奖励.
    # 发送者为 "0" 表明是新挖出的币
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # Forge the new Block by adding it to the chain
    block = blockchain.new_block(proof)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': 'Transaction will be added to Block {index}'.format(index=index)}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(sys.argv[1]))
