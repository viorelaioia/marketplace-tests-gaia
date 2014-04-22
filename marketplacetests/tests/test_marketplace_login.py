# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marketplacetests.marketplace_gaia_test import MarketplaceGaiaTestCase
from gaiatest.mocks.persona_test_user import PersonaTestUser

from marketplacetests.marketplace.app import Marketplace


class TestMarketplaceLogin(MarketplaceGaiaTestCase):

    MARKETPLACE_DEV_NAME = 'Marketplace Dev'

    def setUp(self):
        MarketplaceGaiaTestCase.setUp(self)

        self.user = PersonaTestUser().create_user(verified=True,
                                                  env={"browserid": "firefoxos.persona.org", "verifier": "marketplace-dev.allizom.org"})

        self.marketplace = Marketplace(self.marionette, self.MARKETPLACE_DEV_NAME)
        self.marketplace.launch()

    def test_login_marketplace(self):
        # https://moztrap.mozilla.org/manage/case/4134/

        settings = self.marketplace.tap_settings()
        persona = settings.tap_sign_in()

        persona.login(self.user.email, self.user.password)

        # switch back to Marketplace
        self.marionette.switch_to_frame()
        self.marketplace.launch()

        # wait for signed-in notification at the bottom of the screen to clear
        settings.wait_for_sign_out_button()
        self.marketplace.wait_for_notification_message_not_displayed()

        # Verify that user is logged in
        self.assertEqual(self.user.email, settings.email)

        # Sign out, which should return to the Marketplace home screen
        settings.tap_sign_out()

        # Verify that user is signed out
        settings.wait_for_sign_in_displayed()
