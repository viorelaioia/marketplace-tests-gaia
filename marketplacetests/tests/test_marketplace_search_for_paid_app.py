# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marketplacetests.marketplace_gaia_test import MarketplaceGaiaTestCase
from marketplacetests.marketplace.app import Marketplace


class TestSearchMarketplacePaidApp(MarketplaceGaiaTestCase):

    def test_search_paid_app(self):

        APP_NAME = 'Test Zippy With Me'

        if self.apps.is_app_installed(APP_NAME):
            self.apps.uninstall(APP_NAME)

        marketplace = Marketplace(self.marionette, 'Marketplace Dev')
        marketplace.launch()

        marketplace.set_region('United States')

        search_results = marketplace.search(APP_NAME).search_results

        self.assertGreater(len(search_results), 0, 'No results found.')

        for result in search_results:
            if result.name == APP_NAME:
                saved_price = result.price
                # TODO: Remove this hack once bug https://bugzilla.mozilla.org/show_bug.cgi?id=985508 has been fixed
                try:
                    float(saved_price[2:])
                except ValueError:
                    self.fail(
                        'The app: %s does not appear to be a paid app. Its price is "%s".' %
                        (APP_NAME, saved_price))
                details_page = result.tap_app()
                self.assertEqual(saved_price, details_page.install_button_text)
                return True

        # app not found
        self.fail('The app: %s was not found.' % APP_NAME)
