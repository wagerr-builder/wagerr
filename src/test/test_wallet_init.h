// Copyright (c) 2023 The Wagerr Core developers
// Distributed under the MIT software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#pragma once

#include <wallet/wallet.h>

std::shared_ptr<CWallet> InitTestWallet(const std::string& wallet_name);

extern std::shared_ptr<CWallet> pwallet;

