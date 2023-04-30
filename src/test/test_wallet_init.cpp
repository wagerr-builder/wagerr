// Copyright (c) 2023 The Wagerr Core developers
// Distributed under the MIT software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#include "wallet/wallet.h"
#include "wallet/walletutil.h"
#include "interfaces/chain.h"
#include "interfaces/node.h"
#include "util/translation.h"
#include "node/context.h"
#include "test/test_wallet_init.h"

std::shared_ptr<CWallet> pwallet;

std::shared_ptr<CWallet> InitTestWallet(const std::string& wallet_name) {
    WalletLocation loc(wallet_name);
    std::unique_ptr<NodeContext> node_context = std::make_unique<NodeContext>();
    std::unique_ptr<interfaces::Node> node = interfaces::MakeNode(node_context.get());
    std::unique_ptr<interfaces::Chain> chain = interfaces::MakeChain(*node_context);
    bilingual_str error;
    std::vector<bilingual_str> warnings;
    bool first_run = false;
    pwallet = CWallet::CreateWalletFromFile(*chain, loc, error, warnings, first_run);
    return pwallet;
}


