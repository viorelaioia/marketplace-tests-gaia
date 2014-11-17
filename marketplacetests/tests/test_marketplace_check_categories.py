# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marketplacetests.marketplace_gaia_test import MarketplaceGaiaTestCase
from marketplacetests.marketplace.app import Marketplace


class TestSearchMarketplaceCheckEveryCategory(MarketplaceGaiaTestCase):

    def test_check_every_category_page(self):
        marketplace = Marketplace(self.marionette, self.MARKETPLACE_DEV_NAME)
        marketplace.launch()
        marketplace.show_categories_page()
        for i in range(len(marketplace.categories)):
            category_name = marketplace.categories[i].name
            category = marketplace.categories[i].tap_category()
            self.assertEqual(category_name, category.category_header_name.upper())
            self.assertTrue(len(category.apps_list) > 0)
            category.tap_back()
