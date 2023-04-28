// test_wallet.h

#ifndef TEST_WALLET_H
#define TEST_WALLET_H

#include <wallet/wallet.h>
#include <node/context.h>
#include <node/interfaces.h>

class TestWallet {
public:
    TestWallet();

    std::shared_ptr<CWallet> CreateTestWallet(interfaces::Chain& chain) const;
};

#endif // TEST_WALLET_H
