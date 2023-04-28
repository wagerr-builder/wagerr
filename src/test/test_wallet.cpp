#include "test_wallet.h"

std::shared_ptr<CWallet> TestWallet::CreateTestWallet(TestChain& chain) const {
    WalletLocation wallet_location("test_wallet");
    bool first_run;
    bilingual_str error;
    std::vector<bilingual_str> warning;
    return CWallet::CreateWalletFromFile(chain, wallet_location, error, warning);
}
