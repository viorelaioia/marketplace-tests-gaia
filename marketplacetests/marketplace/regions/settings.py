# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.by import By
from gaiatest.apps.base import Base


class Settings(Base):

    _email_account_field_locator = (By.ID, 'email')
    _save_locator = (By.CSS_SELECTOR, 'footer > p > button')
    _sign_in_button_locator = (By.CSS_SELECTOR, '.only-logged-out a:not(.register)')
    _sign_out_button_locator = (By.CSS_SELECTOR, 'a.button.logout')
    _back_button_locator = (By.ID, 'nav-back')
    _save_changes_button_locator = (By.XPATH, "//section[@id='account-settings']//button[text()='Save Changes']")

    def __init__(self, marionette):
        Base.__init__(self, marionette)
        self.wait_for_element_displayed(*self._sign_in_button_locator)

    def tap_back(self):
        self.marionette.find_element(*self._back_button_locator).tap()
        from marketplacetests.marketplace.app import Marketplace
        return Marketplace(self.marionette)

    def wait_for_sign_in_displayed(self):
        self.wait_for_element_displayed(*self._sign_in_button_locator)

    def tap_sign_in(self):
        self.marionette.find_element(*self._sign_in_button_locator).tap()
        from marketplacetests.firefox_accounts.app import FirefoxAccounts
        return FirefoxAccounts(self.marionette)

    def wait_for_sign_out_button(self):
        self.wait_for_element_displayed(*self._sign_out_button_locator)

    def tap_sign_out(self):
        self.wait_for_sign_out_button()
        self.marionette.find_element(*self._sign_out_button_locator).tap()

    def tap_save_changes(self):
        self.marionette.find_element(*self._save_changes_button_locator).tap()

    @property
    def email(self):
        return self.marionette.find_element(*self._email_account_field_locator).get_attribute('value')
