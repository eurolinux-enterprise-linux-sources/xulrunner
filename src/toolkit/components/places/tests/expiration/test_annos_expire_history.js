/* -*- Mode: C++; tab-width: 2; indent-tabs-mode: nil; c-basic-offset: 2 -*-
 * vim: sw=2 ts=2 et lcs=trail\:.,tab\:>~ :
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/**
 * What this is aimed to test:
 *
 * EXPIRE_WITH_HISTORY annotations should be expired when a page has no more
 * visits, even if the page still exists in the database.
 * This expiration policy is only valid for page annotations.
 */

let os = Cc["@mozilla.org/observer-service;1"].
         getService(Ci.nsIObserverService);
let hs = Cc["@mozilla.org/browser/nav-history-service;1"].
         getService(Ci.nsINavHistoryService);
let bs = Cc["@mozilla.org/browser/nav-bookmarks-service;1"].
         getService(Ci.nsINavBookmarksService);
let as = Cc["@mozilla.org/browser/annotation-service;1"].
         getService(Ci.nsIAnnotationService);

function run_test() {
  // Set interval to a large value so we don't expire on it.
  setInterval(3600); // 1h

  // Expire all expirable pages.
  setMaxPages(0);

  // Add some visited page and a couple expire with history annotations for each.
  let now = getExpirablePRTime();
  for (let i = 0; i < 5; i++) {
    let pageURI = uri("http://page_anno." + i + ".mozilla.org/");
    hs.addVisit(pageURI, now++, null, hs.TRANSITION_TYPED, false, 0);
    as.setPageAnnotation(pageURI, "page_expire1", "test", 0, as.EXPIRE_WITH_HISTORY);
    as.setPageAnnotation(pageURI, "page_expire2", "test", 0, as.EXPIRE_WITH_HISTORY);
  }

  let pages = as.getPagesWithAnnotation("page_expire1");
  do_check_eq(pages.length, 5);
  pages = as.getPagesWithAnnotation("page_expire2");
  do_check_eq(pages.length, 5);

  // Add some bookmarked page and a couple session annotations for each.
  for (let i = 0; i < 5; i++) {
    let pageURI = uri("http://item_anno." + i + ".mozilla.org/");
    // We also add a visit before bookmarking.
    hs.addVisit(pageURI, now++, null, hs.TRANSITION_TYPED, false, 0);
    let id = bs.insertBookmark(bs.unfiledBookmarksFolder, pageURI,
                               bs.DEFAULT_INDEX, null);
    // Notice we use page annotations here, items annotations can't use this
    // kind of expiration policy.
    as.setPageAnnotation(pageURI, "item_persist1", "test", 0, as.EXPIRE_WITH_HISTORY);
    as.setPageAnnotation(pageURI, "item_persist2", "test", 0, as.EXPIRE_WITH_HISTORY);
  }

  let items = as.getPagesWithAnnotation("item_persist1");
  do_check_eq(items.length, 5);
  items = as.getPagesWithAnnotation("item_persist2");
  do_check_eq(items.length, 5);

  // Add other visited page and a couple expire with history annotations for each.
  // We won't expire these visits, so the annotations should survive.
  for (let i = 0; i < 5; i++) {
    let pageURI = uri("http://persist_page_anno." + i + ".mozilla.org/");
    hs.addVisit(pageURI, now++, null, hs.TRANSITION_TYPED, false, 0);
    as.setPageAnnotation(pageURI, "page_persist1", "test", 0, as.EXPIRE_WITH_HISTORY);
    as.setPageAnnotation(pageURI, "page_persist2", "test", 0, as.EXPIRE_WITH_HISTORY);
  }

  pages = as.getPagesWithAnnotation("page_persist1");
  do_check_eq(pages.length, 5);
  pages = as.getPagesWithAnnotation("page_persist2");
  do_check_eq(pages.length, 5);

  // Observe expirations.
  observer = {
    observe: function(aSubject, aTopic, aData) {
      os.removeObserver(observer, PlacesUtils.TOPIC_EXPIRATION_FINISHED);

      let pages = as.getPagesWithAnnotation("page_expire1");
      do_check_eq(pages.length, 0);
      pages = as.getPagesWithAnnotation("page_expire2");
      do_check_eq(pages.length, 0);
      let items = as.getItemsWithAnnotation("item_persist1");
      do_check_eq(items.length, 0);
      items = as.getItemsWithAnnotation("item_persist2");
      do_check_eq(items.length, 0);
      pages = as.getPagesWithAnnotation("page_persist1");
      do_check_eq(pages.length, 5);
      pages = as.getPagesWithAnnotation("page_persist2");
      do_check_eq(pages.length, 5);

      do_test_finished();
    }
  };
  os.addObserver(observer, PlacesUtils.TOPIC_EXPIRATION_FINISHED, false);

  // Expire all visits for the first 5 pages and the bookmarks.
  force_expiration_step(10);
  do_test_pending();
}
