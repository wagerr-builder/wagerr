#!/usr/bin/env python3
# Copyright (c) 2014-2016 The Bitcoin Core developers
# Copyright (c) 2021 The Wagerr Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
"""Test the wallet."""
import sys

from test_framework.test_framework import WagerrTestFramework
from test_framework.util import *
from test_framework.blocktools import *
from test_framework.messages import FromHex, ToHex

MASTERNODE_COLLATERAL = 25000

class WalletTest(WagerrTestFramework):
    def set_test_params(self):
        self.num_nodes = 2
        self.setup_clean_chain = True
        self.extra_args = [['-sporkkey=6xLZdACFRA53uyxz8gKDLcgVrm5kUUEu2B3BUzWUxHqa2W7irbH'],[]]

    def setup_network(self):
        self.add_nodes(2, self.extra_args)
        self.start_node(0)
        self.start_node(1)
        connect_nodes(self.nodes[0],1)
        self.sync_all(self.nodes[0:1])

    def run_test(self):
        self.nodes[0].generate(250)
        mn01_collateral_address = self.nodes[0].getnewaddress()
        mn01_p2p_port = p2p_port(0)
        mn01_blsKey = self.nodes[0].bls('generate')
        mn01_fundsAddr = self.nodes[0].getnewaddress()
        self.nodes[0].sedntoaddress
        mn01_ownerAddr = self.nodes[0].getnewaddress()
        mn01_operatorAddr = mn01_blsKey['public']
        mn01_votingAddr = mn01_ownerAddr
#        mn01_blsMnkey = mn01_blsKey['secret']

        txid=self.nodes[0].sendtoaddress(mn01_fundsAddr, MASTERNODE_COLLATERAL)
        collateral_vout = 0
        txraw = self.nodes[0].getrawtransaction(txid, True)
        for vout_idx in range(0, len(txraw["vout"])):
            vout = txraw["vout"][vout_idx]
            if vout["value"] == MASTERNODE_COLLATERAL:
                collateral_vout = vout_idx
        self.nodes[0].lockunspent(False, [{'txid': txid, 'vout': collateral_vout}])
        self.nodes[0].generate(1)
        self.nodes[0].sendtoaddress(mn01_fundsAddr, 0.001)
        mn01_collateral_address = self.nodes[0].getnewaddress()
        mn01_rewards_address = self.nodes[0].getnewaddress()

        self.log.info(mn01_collateral_address)
        self.log.info('127.0.0.1:%d' % mn01_p2p_port)
        self.log.info(mn01_ownerAddr)
        self.log.info(mn01_operatorAddr)
        self.log.info(mn01_votingAddr)
        self.log.info(mn01_rewards_address)
        self.log.info(mn01_fundsAddr)

        self.nodes[0].generate(250)
        mn01_protx_hash = self.nodes[0].protx('register', txid, collateral_vout,  '127.0.0.1:%d' % mn01_p2p_port, mn01_ownerAddr, mn01_operatorAddr, mn01_votingAddr, 0, mn01_rewards_address, mn01_fundsAddr, True)

        mn01_collateral_txid = mn01_protx_hash
        mn01_collateral_vout = -1

        rawtx = self.nodes[0].getrawtransaction(mn01_collateral_txid, 1)
        for txout in rawtx['vout']:
            self.log.info("TxOut %s"  % txout)
            if txout['value'] == Decimal(25000):
                mn01_collateral_vout = txout['n']
                break
        breakpoint()
        assert(mn01_collateral_vout != -1)

        self.log.info("mn01_protx_hash:")
        self.log.info(mn01_protx_hash)
        disconnect_nodes(0,1) 
        disconnect_nodes(1,0) 
        time.sleep(10)
        connect_nodes(self.nodes[0] ,1)
        self.sync_all()
        self.nodes[0].spork("SPORK_4_DIP0003_ENFORCED", self.nodes[0].getblockcount() + 1)
        self.wait_for_sporks_same()
        self.sync_all()

        self.nodes[0].generate(2)

        self.log.info(self.nodes[0].masternode('list'))

    def cutoff(self):
        self.log.info("Done")


if __name__ == '__main__':
    WalletTest().main()
