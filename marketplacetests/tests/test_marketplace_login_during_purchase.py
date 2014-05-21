# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest.mocks.persona_test_user import PersonaTestUser
from marionette.errors import StaleElementException
from marionette.wait import Wait

from marketplacetests.marketplace_gaia_test import MarketplaceGaiaTestCase
from marketplacetests.marketplace.app import Marketplace


class TestMarketplaceLoginDuringPurchase(MarketplaceGaiaTestCase):

    def test_purchase_app(self):

        APP_NAME = 'Test Zippy With Me'

        if self.apps.is_app_installed(APP_NAME):
            self.apps.uninstall(APP_NAME)

        user = PersonaTestUser().create_user(verified=True,
                                             env={"browserid": "firefoxos.persona.org",
                                                  "verifier": "marketplace-dev.allizom.org"})
        marketplace = Marketplace(self.marionette, 'Marketplace Dev')
        marketplace.launch()

        marketplace.set_region('United States')

        details_page = marketplace.navigate_to_app(APP_NAME)
        persona = details_page.tap_purchase_button(is_logged_in=False)
        persona.login(user.email, user.password)

        # Switch back to the Marketplace frame and wait for the install button to update
        marketplace.launch()
        Wait(marionette=self.marionette, ignored_exceptions=StaleElementException)\
            .until(lambda m: details_page.install_button_text == 'Purchasing')
