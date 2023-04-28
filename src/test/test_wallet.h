// test_wallet.h

#ifndef TEST_WALLET_H
#define TEST_WALLET_H

#include <wallet/wallet.h>

class TestWallet {
public:
    TestWallet();

    std::shared_ptr<CWallet> CreateTestWallet() const;
};

#endif // TEST_WALLET_H
