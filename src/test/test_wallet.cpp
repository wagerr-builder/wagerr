// test_wallet.cpp

#include <test/test_wallet.h>

TestWallet::TestWallet() {
    // You can initialize any required data here, if necessary
}

std::shared_ptr<CWallet> TestWallet::CreateTestWallet() const {
    // Customize the wallet creation process according to your requirements
    std::string wallet_file = "wallet.dat";
    std::string error;
    std::string warning;

    bool first_run;
    auto wallet = CWallet::CreateWalletFromFile(wallet_file, first_run, error, warning);
    if (!wallet) {
        throw std::runtime_error(strprintf("CreateTestWa;;et : unable to create wallet"));
    }

    // Perform any additional setup or configuration for the test wallet

    return wallet;
}
