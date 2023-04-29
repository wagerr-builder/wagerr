#include "test_wallet_init.h"
#include <wallet/wallet.h>

std::shared_ptr<CWallet> pwallet;

void InitTestWallet(const std::string& wallet_name) {
    WalletLocation loc(wallet_name);
    std::string error;
    std::string warning;
    bool first_run;
    pwallet = CWallet::CreateWalletFromFile(loc, error, warning, first_run);
    if (!pwallet) {
        throw std::runtime_error(strprintf("Failed to create wallet: %s", error));
    }
}
