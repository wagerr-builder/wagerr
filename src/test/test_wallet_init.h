#pragma once

#include "wallet/wallet.h"

std::shared_ptr<CWallet> InitTestWallet(const std::string& wallet_name);

extern std::shared_ptr<CWallet> pwallet;

