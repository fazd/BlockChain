import numpy as np
from BlockChain import BlockChain

def isChainValid(ChainBlock):
    ant = ChainBlock.chain[0]
    for i in ChainBlock.chain[1:]:
        if(not (i.prevHash == ant.hash)):
            return False
        ant = i
    return True