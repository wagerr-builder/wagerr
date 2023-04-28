// test_wallet.h

#ifndef TEST_WALLET_H
#define TEST_WALLET_H

#include "wallet/wallet.h"
#include "test/test_chain.h" // Add this include

class TestWallet {
public:
    TestWallet() = default;
    std::shared_ptr<CWallet> CreateTestWallet(TestChain& chain) const;
};

#endif // TEST_WALLET_H
