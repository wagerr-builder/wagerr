#!/usr/bin/env python3
# Copyright (c) 2020-2022 The Wagerr Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
from test_framework.test_framework import WagerrTestFramework
from test_framework.util import assert_equal, get_bip9_status

'''
feature_new_quorum_type_activation.py

Tests the activation of a new quorum type in dip0020 via a bip9-like hardfork

'''


class NewQuorumTypeActivationTest(WagerrTestFramework):
    def set_test_params(self):
        #self.extra_args = [["-vbparams=dip0020:0:999999999999:10:8:6:5"]]
        extra_args = [["-sporkkey=6xLZdACFRA53uyxz8gKDLcgVrm5kUUEu2B3BUzWUxHqa2W7irbH"]] * 4
        self.set_wagerr_test_params(4, 3, extra_args=extra_args, fast_dip3_enforcement=False)

    def run_test(self):
        for i in range(len(self.nodes)):
                self.nodes[i].sporkupdate("SPORK_4_DIP0003_ENFORCED", 1)
                self.nodes[i].sporkupdate("SPORK_17_QUORUM_DKG_ENABLED", 1)
                self.nodes[i].sporkupdate("SPORK_21_QUORUM_ALL_CONNECTED", 1)
                self.nodes[i].sporkupdate("SPORK_23_QUORUM_POSE", 1)

        self.wait_for_sporks_same()
        #assert_equal(get_bip9_status(self.nodes[0], 'dip0020')['status'], 'defined')
        self.nodes[0].generate(9)
        #assert_equal(get_bip9_status(self.nodes[0], 'dip0020')['status'], 'started')
        ql = self.nodes[0].quorum("list")
        assert_equal(len(ql), 4)
        assert "llmq_test_v18" in ql
        self.nodes[0].generate(300)
        breakpoint()
        #assert_equal(get_bip9_status(self.nodes[0], 'dip0020')['status'], 'locked_in')
        ql = self.nodes[0].quorum("list")
        assert_equal(len(ql), 2)
        assert "llmq_test_v18" not in ql
        self.nodes[0].generate(10)
        #assert_equal(get_bip9_status(self.nodes[0], 'dip0020')['status'], 'active')
        ql = self.nodes[0].quorum("list")
        assert_equal(len(ql), 3)
        assert "llmq_test_v18" in ql


if __name__ == '__main__':
    NewQuorumTypeActivationTest().main()
