#!/usr/bin/env python3
# Copyright (c) 2014-2015 The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

#
# Test addressindex generation and fetching
#

import binascii

from test_framework.messages import COIN, COutPoint, CTransaction, CTxIn, CTxOut
from test_framework.test_framework import WagerrTestFramework
from test_framework.test_node import ErrorMatch
from test_framework.script import CScript, OP_CHECKSIG, OP_DUP, OP_EQUAL, OP_EQUALVERIFY, OP_HASH160
from test_framework.util import assert_equal, connect_nodes, disconnect_nodes

class AddressIndexTest(WagerrTestFramework):

    def set_test_params(self):
        self.setup_clean_chain = True
        self.num_nodes = 4
        self.supports_cli = False

    def skip_test_if_missing_module(self):
        self.skip_if_no_wallet()

    def setup_network(self):
        self.add_nodes(self.num_nodes)
        # Nodes 0/1 are "wallet" nodes
        self.start_node(0, [])
        self.start_node(1, ["-addressindex"])
        # Nodes 2/3 are used for testing
        self.start_node(2, ["-addressindex"])
        self.start_node(3, ["-addressindex"])
        connect_nodes(self.nodes[0], 1)
        connect_nodes(self.nodes[0], 2)
        connect_nodes(self.nodes[0], 3)
        self.sync_all()
        #self.import_deterministic_coinbase_privkeys()

    def run_test(self):
        self.log.info("Test that settings can't be changed without -reindex...")
        self.stop_node(1)
        self.nodes[1].assert_start_raises_init_error(["-addressindex=0"], "You need to rebuild the database using -reindex to change -addressindex", partial_match=True)
        self.start_node(1, ["-addressindex=0", "-reindex"])
        connect_nodes(self.nodes[0], 1)
        self.sync_all()
        self.stop_node(1)
        self.nodes[1].assert_start_raises_init_error(["-addressindex"], "You need to rebuild the database using -reindex to change -addressindex", partial_match=True)
        self.start_node(1, ["-addressindex", "-reindex"])
        connect_nodes(self.nodes[0], 1)
        self.sync_all()

        self.log.info("Mining blocks...")
        mining_address = self.nodes[0].getnewaddress()
        sendto_address = self.nodes[1].getnewaddress()
        self.nodes[0].generate(150)
        for n in range(self.num_nodes):
            self.stop_node(n)
        self.start_node(0, ["-reindex"])
        self.start_node(1, ["-addressindex", "-reindex"])
        self.start_node(2, ["-reindex"])
        self.start_node(3, ["-reindex"])
        disconnect_nodes(self.nodes[0], 1)
        connect_nodes(self.nodes[0], 1)
        disconnect_nodes(self.nodes[0], 2)
        connect_nodes(self.nodes[0], 2)
        disconnect_nodes(self.nodes[0], 3)
        connect_nodes(self.nodes[0], 3)
        self.sync_all()

        chain_height = self.nodes[1].getblockcount()
        assert_equal(chain_height, 150)
        assert_equal(self.nodes[1].getbalance(), 0)
        assert_equal(self.nodes[2].getbalance(), 0)

        # Check that balances are correct
        balance0 = self.nodes[1].getbalance()
        balance_mining = self.nodes[0].getwalletinfo()
        assert_equal(balance0, 0)
        assert_equal(balance_mining["balance"], 207860471)
        assert_equal(balance_mining["immature_balance"], 2500000)
        assert_equal((balance_mining["balance"] - balance_mining["immature_balance"]), 205360471)

        # Check p2pkh and p2sh address indexes
        self.log.info("Testing p2pkh and p2sh address index...")

        txid0 = self.nodes[0].sendtoaddress("TTzu4XKjnSeWPVJHmrWw5uaApihdRxQrB7", 10)
        self.nodes[0].generate(1)

        txidb0 = self.nodes[0].sendtoaddress(sendto_address, 10)
        self.nodes[0].generate(1)

        txid1 = self.nodes[0].sendtoaddress("TTzu4XKjnSeWPVJHmrWw5uaApihdRxQrB7", 15)
        self.nodes[0].generate(1)

        txidb1 = self.nodes[0].sendtoaddress(sendto_address, 15)
        self.nodes[0].generate(1)

        txid2 = self.nodes[0].sendtoaddress("TTzu4XKjnSeWPVJHmrWw5uaApihdRxQrB7", 20)
        self.nodes[0].generate(1)

        txidb2 = self.nodes[0].sendtoaddress(sendto_address, 20)
        self.nodes[0].generate(1)

        self.sync_all()

        txids = self.nodes[1].getaddresstxids("TTzu4XKjnSeWPVJHmrWw5uaApihdRxQrB7")
        assert_equal(len(txids), 3)
        assert_equal(txids[0], txid0)
        assert_equal(txids[1], txid1)
        assert_equal(txids[2], txid2)

        txidsb = self.nodes[1].getaddresstxids(sendto_address)
        assert_equal(len(txidsb), 3)
        assert_equal(txidsb[0], txidb0)
        assert_equal(txidsb[1], txidb1)
        assert_equal(txidsb[2], txidb2)

        # Check that limiting by height works
        self.log.info("Testing querying txids by range of block heights..")
        height_txids = self.nodes[1].getaddresstxids({
            "addresses": [sendto_address],
            "start": 150,
            "end": 155
        })
        assert_equal(len(height_txids), 2)
        assert_equal(height_txids[0], txidb0)
        assert_equal(height_txids[1], txidb1)

        # Check that multiple addresses works
        multitxids = self.nodes[1].getaddresstxids({"addresses": [sendto_address, "TTzu4XKjnSeWPVJHmrWw5uaApihdRxQrB7"]})
        assert_equal(len(multitxids), 6)
        assert_equal(multitxids[0], txid0)
        assert_equal(multitxids[1], txidb0)
        assert_equal(multitxids[2], txid1)
        assert_equal(multitxids[3], txidb1)
        assert_equal(multitxids[4], txid2)
        assert_equal(multitxids[5], txidb2)

        # Check that balances are correct
        balance0 = self.nodes[1].getaddressbalance(sendto_address)
        assert_equal(balance0["balance"], 45 * 100000000)

        # Check that outputs with the same address will only return one txid
        self.log.info("Testing for txid uniqueness...")
        addressHash = binascii.unhexlify("FE30B718DCF0BF8A2A686BF1820C073F8B2C3B37")
        scriptPubKey = CScript([OP_HASH160, addressHash, OP_EQUAL])
        unspent = self.nodes[0].listunspent()
        tx = CTransaction()
        tx.vin = [CTxIn(COutPoint(int(unspent[0]["txid"], 16), unspent[0]["vout"]))]
        tx.vout = [CTxOut(10 * COIN, scriptPubKey), CTxOut(11 * COIN, scriptPubKey)]
        tx.rehash()

        signed_tx = self.nodes[0].signrawtransactionwithwallet(tx.serialize().hex())
        sent_txid = self.nodes[0].sendrawtransaction(signed_tx["hex"], 0)

        self.nodes[0].generate(1)
        self.sync_all()

        txidsmany = self.nodes[1].getaddresstxids(sendto_address)
        assert_equal(len(txidsmany), 3)
        #assert_equal(txidsmany[2], sent_txid)

        # Check that balances are correct
        self.log.info("Testing balances...")
        balance0 = self.nodes[1].getaddressbalance(sendto_address)
        assert_equal(balance0["balance"], 45 * 100000000)

        # Check that balances are correct after spending
        self.log.info("Testing balances after spending...")
        privkey2 = "THTeyaP8QLTG8zwG1AdYrnWqCaaAjbj7TcW9xRhJ7n6LRLCeg6Bc"
        address2 = "TPEdK89Rwds4rxdbBApYCKM6AQPcDZf8qh"
        addressHash2 = binascii.unhexlify("91842b36d6fd19e6077c28fb086964f818f5114f")
        scriptPubKey2 = CScript([OP_DUP, OP_HASH160, addressHash2, OP_EQUALVERIFY, OP_CHECKSIG])
        self.nodes[0].importprivkey(privkey2)

        unspent = self.nodes[0].listunspent()
        tx = CTransaction()
        tx_fee_sat = 2000
        tx.vin = [CTxIn(COutPoint(int(unspent[0]["txid"], 16), unspent[0]["vout"]))]
        amount = int(unspent[0]["amount"] * 100000000) - tx_fee_sat
        tx.vout = [CTxOut(amount, scriptPubKey2)]
        tx.rehash()
        signed_tx = self.nodes[0].signrawtransactionwithwallet(tx.serialize().hex())
        spending_txid = self.nodes[0].sendrawtransaction(signed_tx["hex"], 0)
        self.nodes[0].generate(1)
        self.sync_all()
        balance1 = self.nodes[1].getaddressbalance(address2)
        assert_equal(balance1["balance"], amount)

        tx = CTransaction()
        tx.vin = [CTxIn(COutPoint(int(spending_txid, 16), 0))]
        send_amount = 1 * 100000000 + 12840
        change_amount = amount - send_amount - 10000
        tx.vout = [CTxOut(change_amount, scriptPubKey2), CTxOut(send_amount, scriptPubKey)]
        tx.rehash()

        signed_tx = self.nodes[0].signrawtransactionwithwallet(tx.serialize().hex())
        sent_txid = self.nodes[0].sendrawtransaction(signed_tx["hex"], 0)
        self.nodes[0].generate(1)
        self.sync_all()

        balance2 = self.nodes[1].getaddressbalance(address2)
        assert_equal(balance2["balance"], change_amount)

        # Check that deltas are returned correctly
        deltas = self.nodes[1].getaddressdeltas({"addresses": [address2], "start": 0, "end": 200})
        balance3 = 0
        for delta in deltas:
            balance3 += delta["satoshis"]
        assert_equal(balance3, change_amount)
        assert_equal(deltas[0]["address"], address2)
        assert_equal(deltas[0]["blockindex"], 1)

        # Check that entire range will be queried
        deltasAll = self.nodes[1].getaddressdeltas({"addresses": [address2]})
        assert_equal(len(deltasAll), len(deltas))

        # Check that deltas can be returned from range of block heights
        breakpoint()
        deltas = self.nodes[1].getaddressdeltas({"addresses": [address2], "start": 158, "end": 158})
        assert_equal(len(deltas), 1)

        # Check that unspent outputs can be queried
        self.log.info("Testing utxos...")
        utxos = self.nodes[1].getaddressutxos({"addresses": [address2]})
        assert_equal(len(utxos), 1)
        assert_equal(utxos[0]["satoshis"], change_amount)

        # Check that indexes will be updated with a reorg
        self.log.info("Testing reorg...")

        best_hash = self.nodes[0].getbestblockhash()
        self.nodes[0].invalidateblock(best_hash)
        self.nodes[1].invalidateblock(best_hash)
        self.nodes[2].invalidateblock(best_hash)
        self.nodes[3].invalidateblock(best_hash)
        # Allow some time for the reorg to start
        self.bump_mocktime(2)
        self.sync_all()

        balance4 = self.nodes[1].getaddressbalance(address2)
        assert_equal(balance4, balance1)

        utxos2 = self.nodes[1].getaddressutxos({"addresses": [address2]})
        assert_equal(len(utxos2), 1)
        assert_equal(utxos2[0]["satoshis"], amount)

        # Check sorting of utxos
        self.nodes[2].generate(150)

        self.nodes[2].sendtoaddress(address2, 50)
        self.nodes[2].generate(1)
        self.nodes[2].sendtoaddress(address2, 50)
        self.nodes[2].generate(1)
        self.sync_all()

        utxos3 = self.nodes[1].getaddressutxos({"addresses": [address2]})
        assert_equal(len(utxos3), 3)
        assert_equal(utxos3[0]["height"], 159)
        assert_equal(utxos3[1]["height"], 264)
        assert_equal(utxos3[2]["height"], 265)

        # Check mempool indexing
        self.log.info("Testing mempool indexing...")

        privKey3 = "TFqoWjmdn8jiYSsiMokrDXpMbuXYQLkrBFmcrQraCvRzYad8z3ta"
        address3 = "TMLm1DCB3wtxNdEUZ5P8gb1KEBP5ZGFATy"
        addressHash3 = binascii.unhexlify("7cbcd550a9861e9e80dd4598031e1475f1015c06")
        scriptPubKey3 = CScript([OP_DUP, OP_HASH160, addressHash3, OP_EQUALVERIFY, OP_CHECKSIG])
        # address4 = "2N8oFVB2vThAKury4vnLquW2zVjsYjjAkYQ"
        scriptPubKey4 = CScript([OP_HASH160, addressHash3, OP_EQUAL])
        unspent = self.nodes[2].listunspent()

        tx = CTransaction()
        tx.vin = [CTxIn(COutPoint(int(unspent[0]["txid"], 16), unspent[0]["vout"]))]
        amount = int(unspent[0]["amount"] * 100000000) - tx_fee_sat
        tx.vout = [CTxOut(amount, scriptPubKey3)]
        tx.rehash()
        signed_tx = self.nodes[2].signrawtransactionwithwallet(tx.serialize().hex())
        memtxid1 = self.nodes[2].sendrawtransaction(signed_tx["hex"], 0)
        self.bump_mocktime(2)

        tx2 = CTransaction()
        tx_fee_sat = 3000
        tx2.vin = [CTxIn(COutPoint(int(unspent[1]["txid"], 16), unspent[1]["vout"]))]
        amount = int(unspent[1]["amount"] * 100000000) - tx_fee_sat
        tx2.vout = [
            CTxOut(int(amount / 4), scriptPubKey3),
            CTxOut(int(amount / 4), scriptPubKey3),
            CTxOut(int(amount / 4), scriptPubKey4),
            CTxOut(int(amount / 4), scriptPubKey4)
        ]
        tx2.rehash()
        signed_tx2 = self.nodes[2].signrawtransactionwithwallet(tx2.serialize().hex())
        memtxid2 = self.nodes[2].sendrawtransaction(signed_tx2["hex"], 0)
        self.bump_mocktime(2)

        mempool = self.nodes[2].getaddressmempool({"addresses": [address3]})
        assert_equal(len(mempool), 3)
        assert_equal(mempool[0]["txid"], memtxid1)
        assert_equal(mempool[0]["address"], address3)
        assert_equal(mempool[0]["index"], 0)
        assert_equal(mempool[1]["txid"], memtxid2)
        assert_equal(mempool[1]["index"], 0)
        assert_equal(mempool[2]["txid"], memtxid2)
        assert_equal(mempool[2]["index"], 1)

        self.nodes[2].generate(1)
        self.sync_all()
        mempool2 = self.nodes[2].getaddressmempool({"addresses": [address3]})
        assert_equal(len(mempool2), 0)

        tx = CTransaction()
        tx.vin = [
            CTxIn(COutPoint(int(memtxid2, 16), 0)),
            CTxIn(COutPoint(int(memtxid2, 16), 1))
        ]
        tx.vout = [CTxOut(int(amount / 2 - 10000), scriptPubKey2)]
        tx.rehash()
        self.nodes[2].importprivkey(privKey3)
        signed_tx3 = self.nodes[2].signrawtransactionwithwallet(tx.serialize().hex())
        self.nodes[2].sendrawtransaction(signed_tx3["hex"], 0)
        self.bump_mocktime(2)

        mempool3 = self.nodes[2].getaddressmempool({"addresses": [address3]})
        assert_equal(len(mempool3), 2)
        assert_equal(mempool3[0]["prevtxid"], memtxid2)
        assert_equal(mempool3[0]["prevout"], 0)
        assert_equal(mempool3[1]["prevtxid"], memtxid2)
        assert_equal(mempool3[1]["prevout"], 1)

        # sending and receiving to the same address
        privkey1 = "TCiM4JqGNtShSZfSop7CEhSQzWNXXoony1yumWvW5gN5imKYp47E"
        address1 = "TLS3RUwUvDoFhkT8yScNJWzqX1eHBTRdH6"
        address1hash = binascii.unhexlify("0909C84A817651502E020AAD0FBCAE5F656E7D8A")
        address1script = CScript([OP_DUP, OP_HASH160, address1hash, OP_EQUALVERIFY, OP_CHECKSIG])

        self.nodes[0].sendtoaddress(address1, 10)
        self.nodes[0].generate(1)
        self.sync_all()

        utxos = self.nodes[1].getaddressutxos({"addresses": [address1]})
        assert_equal(len(utxos), 1)

        tx = CTransaction()
        tx.vin = [
            CTxIn(COutPoint(int(utxos[0]["txid"], 16), utxos[0]["outputIndex"]))
        ]
        amount = int(utxos[0]["satoshis"] - 10000)
        tx.vout = [CTxOut(amount, address1script)]
        tx.rehash()
        self.nodes[0].importprivkey(privkey1)
        signed_tx = self.nodes[0].signrawtransactionwithwallet(tx.serialize().hex())
        self.nodes[0].sendrawtransaction(signed_tx["hex"], 0)

        self.sync_all()
        mempool_deltas = self.nodes[2].getaddressmempool({"addresses": [address1]})
        assert_equal(len(mempool_deltas), 1)

        self.log.info("Passed")


if __name__ == '__main__':
    AddressIndexTest().main()
