#pragma once

#ifdef IS_TEST_ENVIRONMENT
    #define IS_TEST_ENVIRONMENT_MACRO true
#else
    #define IS_TEST_ENVIRONMENT_MACRO false
#endif
