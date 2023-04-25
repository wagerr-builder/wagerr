// Copyright (c) 2023 The Wagerr developers
// Distributed under the MIT/X11 software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#pragma once

inline bool IsTestEnvironment() {
#ifdef IS_TEST_ENVIRONMENT
    return true;
#else
    return false;
#endif
}