#include "wallet/wallet.h"
#include "wallet/walletutil.h"
#include "interfaces/chain.h"
#include "test/interfaces.h"
#include "test_wallet_init.h"

std::shared_ptr<CWallet> pwallet;

void InitTestWallet(const std::string& wallet_name) {
    WalletLocation loc(wallet_name);

    std::unique_ptr<interfaces::Chain> chain = interfaces::MakeChain();
    bilingual_str error;
    std::vector<bilingual_str> warnings;
    bool first_run = false;
    pwallet = CWallet::CreateWalletFromFile(*chain, loc, error, warnings, first_run);
}
