# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from fxapom.fxapom import FxATestAccount
from marketplacetests.firefox_accounts.app import FirefoxAccounts
from marketplacetests.payment.app import Payment
from marketplacetests.marketplace_gaia_test import MarketplaceGaiaTestCase
from marketplacetests.marketplace.app import Marketplace


class TestMarketplaceForgetPin(MarketplaceGaiaTestCase):

    def test_marketplace_forget_pin(self):
        APP_NAME = 'Test Zippy With Me'
        PIN = '1234'
        NEW_PIN = '5678'
        acct = FxATestAccount(base_url=self.base_url).create_account()

        if self.apps.is_app_installed(APP_NAME):
            self.apps.uninstall(APP_NAME)

        marketplace = Marketplace(self.marionette, self.MARKETPLACE_DEV_NAME)
        marketplace.launch()

        marketplace.set_region('United States')

        details_page = marketplace.navigate_to_app(APP_NAME)
        details_page.tap_install_button()

        ff_accounts = FirefoxAccounts(self.marionette)
        password = acct.password
        ff_accounts.login(acct.email, acct.password)

        payment = Payment(self.marionette)
        payment.create_pin(PIN)
        payment.wait_for_buy_app_section_displayed()
        payment.tap_cancel_button()
        marketplace.switch_to_marketplace_frame()
        marketplace.wait_for_notification_message_not_displayed()

        details_page.tap_install_button()
        payment.tap_forgot_pin()
        payment.tap_reset_button()
        ff_accounts.type_password(password)
        ff_accounts.tap_sign_in(second_login=True)
        payment.create_pin(NEW_PIN)
        payment.wait_for_buy_app_section_displayed()
        self.assertIn(APP_NAME, payment.app_name)
