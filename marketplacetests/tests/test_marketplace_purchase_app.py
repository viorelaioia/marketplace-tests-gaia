# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest.apps.homescreen.regions.confirm_install import ConfirmInstall
from gaiatest.mocks.persona_test_user import PersonaTestUser

from marketplacetests.marketplace_gaia_test import MarketplaceGaiaTestCase
from marketplacetests.marketplace.app import Marketplace


class TestMarketplacePurchaseApp(MarketplaceGaiaTestCase):

    def test_purchase_app(self):

        APP_NAME = 'Test Zippy With Me'
        PIN = '1234'

        if self.apps.is_app_installed(APP_NAME):
            self.apps.uninstall(APP_NAME)

        user = PersonaTestUser().create_user(verified=True,
                                             env={"browserid": "firefoxos.persona.org",
                                                  "verifier": "marketplace-dev.allizom.org"})
        marketplace = Marketplace(self.marionette, 'Marketplace Dev')
        marketplace.launch()

        marketplace.login(user)

        marketplace.set_region('United States')

        details_page = marketplace.navigate_to_app(APP_NAME)
        payment = details_page.tap_purchase_button()

        payment.create_pin(PIN)
        payment.wait_for_buy_app_section_displayed()
        self.assertIn(APP_NAME, payment.app_name)
        payment.tap_buy_button()

        # Confirm the installation and wait for the app icon to be present
        confirm_install = ConfirmInstall(self.marionette)
        confirm_install.tap_confirm()

        self.assertEqual('%s installed' % APP_NAME, marketplace.install_notification_message)
        marketplace.launch()
        self.assertEqual('Launch', details_page.install_button_text)
