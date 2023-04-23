// Copyright (c) 2023 The Wagerr developers
// Distributed under the MIT/X11 software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#include "betting_view_init.h"

CBettingsView* initializeBettingView(std::unique_ptr<CBettingsView> &bettingsView, bool fReindex) {
    // Reset bettingsView
    bettingsView.reset(new CBettingsView());

    bettingsView->mappingsStorage = MakeUnique<CStorageLevelDB>(CBettingDB::MakeDbPath("mappings"), CBettingDB::dbWrapperCacheSize(), false, fReindex);        // create cacheble betting DB with LevelDB storage as main storage
    bettingsView->mappings = MakeUnique<CBettingDB>(*bettingsView->mappingsStorage.get());

    bettingsView->eventsStorage = MakeUnique<CStorageLevelDB>(CBettingDB::MakeDbPath("events"), CBettingDB::dbWrapperCacheSize(), false, fReindex);
    bettingsView->events = MakeUnique<CBettingDB>(*bettingsView->eventsStorage.get());

    bettingsView->resultsStorage = MakeUnique<CStorageLevelDB>(CBettingDB::MakeDbPath("results"), CBettingDB::dbWrapperCacheSize(), false, fReindex);
    bettingsView->results = MakeUnique<CBettingDB>(*bettingsView->resultsStorage.get());

    bettingsView->betsStorage = MakeUnique<CStorageLevelDB>(CBettingDB::MakeDbPath("bets"), CBettingDB::dbWrapperCacheSize(), false, fReindex);
    bettingsView->bets = MakeUnique<CBettingDB>(*bettingsView->betsStorage.get());

    bettingsView->fieldEventsStorage = MakeUnique<CStorageLevelDB>(CBettingDB::MakeDbPath("fieldevents"), CBettingDB::dbWrapperCacheSize(), false, fReindex);
    bettingsView->fieldEvents = MakeUnique<CBettingDB>(*bettingsView->fieldEventsStorage.get());

    bettingsView->fieldResultsStorage = MakeUnique<CStorageLevelDB>(CBettingDB::MakeDbPath("fieldresults"), CBettingDB::dbWrapperCacheSize(), false, fReindex);
    bettingsView->fieldResults = MakeUnique<CBettingDB>(*bettingsView->fieldResultsStorage.get());

    bettingsView->fieldBetsStorage = MakeUnique<CStorageLevelDB>(CBettingDB::MakeDbPath("fieldbets"), CBettingDB::dbWrapperCacheSize(), false, fReindex);
    bettingsView->fieldBets = MakeUnique<CBettingDB>(*bettingsView->fieldBetsStorage.get());

    bettingsView->undosStorage = MakeUnique<CStorageLevelDB>(CBettingDB::MakeDbPath("undos"), CBettingDB::dbWrapperCacheSize(), false, fReindex);
    bettingsView->undos = MakeUnique<CBettingDB>(*bettingsView->undosStorage.get());

    bettingsView->payoutsInfoStorage = MakeUnique<CStorageLevelDB>(CBettingDB::MakeDbPath("payoutsinfo"), CBettingDB::dbWrapperCacheSize(), false, fReindex);
    bettingsView->payoutsInfo = MakeUnique<CBettingDB>(*bettingsView->payoutsInfoStorage.get());

    bettingsView->quickGamesBetsStorage = MakeUnique<CStorageLevelDB>(CBettingDB::MakeDbPath("quickgamesbets"), CBettingDB::dbWrapperCacheSize(), false, fReindex);
    bettingsView->quickGamesBets = MakeUnique<CBettingDB>(*bettingsView->quickGamesBetsStorage.get());

    bettingsView->chainGamesLottoEventsStorage = MakeUnique<CStorageLevelDB>(CBettingDB::MakeDbPath("cglottoevents"), CBettingDB::dbWrapperCacheSize(), false, fReindex);
    bettingsView->chainGamesLottoEvents = MakeUnique<CBettingDB>(*bettingsView->chainGamesLottoEventsStorage.get());

    bettingsView->chainGamesLottoBetsStorage = MakeUnique<CStorageLevelDB>(CBettingDB::MakeDbPath("cglottobets"), CBettingDB::dbWrapperCacheSize(), false, fReindex);
    bettingsView->chainGamesLottoBets = MakeUnique<CBettingDB>(*bettingsView->chainGamesLottoBetsStorage.get());

    bettingsView->chainGamesLottoResultsStorage = MakeUnique<CStorageLevelDB>(CBettingDB::MakeDbPath("cglottoresults"), CBettingDB::dbWrapperCacheSize(), false, fReindex);
    bettingsView->chainGamesLottoResults = MakeUnique<CBettingDB>(*bettingsView->chainGamesLottoResultsStorage.get());

    bettingsView->failedBettingTxsStorage = MakeUnique<CStorageLevelDB>(CBettingDB::MakeDbPath("failedtxs"), CBettingDB::dbWrapperCacheSize(), false, fReindex);
    bettingsView->failedBettingTxs = MakeUnique<CBettingDB>(*bettingsView->failedBettingTxsStorage.get());

    return bettingsView.get();
}
