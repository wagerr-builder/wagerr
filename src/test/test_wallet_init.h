#pragma once

#include "wallet/wallet.h"

void InitTestWallet(const std::string& wallet_name);

extern std::shared_ptr<CWallet> pwallet;

