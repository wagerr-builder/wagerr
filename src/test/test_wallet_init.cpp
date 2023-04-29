#include "wallet/wallet.h"
#include "wallet/walletutil.h"
#include "interfaces/chain.h"
#include "interfaces/node.h"
#include "util/translation.h" // <-- Include the header for bilingual_str
#include "node/context.h"
#include "test/test_wallet_init.h"

std::shared_ptr<CWallet> pwallet;

void InitTestWallet(const std::string& wallet_name) {
    WalletLocation loc(wallet_name);

    std::unique_ptr<interfaces::Node> node = MakeNode();
    std::unique_ptr<interfaces::Chain> chain = interfaces::MakeChain(*node);
    bilingual_str error;
    std::vector<bilingual_str> warnings;
    bool first_run = false;
    pwallet = CWallet::CreateWalletFromFile(*chain, loc, error, warnings, first_run);
}

std::unique_ptr<interfaces::Node> MakeNode() {
    std::unique_ptr<NodeContext> node_context = std::make_unique<NodeContext>();
    std::unique_ptr<interfaces::Node> node = interfaces::MakeNode(*node_context);
    return node;
}


