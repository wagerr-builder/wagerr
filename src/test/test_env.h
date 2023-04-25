// Copyright (c) 2023 The Wagerr developers
// Distributed under the MIT/X11 software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#pragma once

#ifdef IS_TEST_ENVIRONMENT
    #define IS_TEST_ENVIRONMENT_MACRO true
#else
    #define IS_TEST_ENVIRONMENT_MACRO false
#endif
