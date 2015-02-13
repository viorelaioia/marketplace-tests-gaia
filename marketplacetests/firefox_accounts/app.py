# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.by import By
from gaiatest.apps.base import Base


class FirefoxAccounts(Base):

    # iframe
    _in_app_login_frame_locator = (By.CSS_SELECTOR, '#trustedui-inner iframe')
    _ff_accounts_frame_locator = (By.CSS_SELECTOR, "iframe[name='fxa']")

    # firefox accounts login
    _body_loading_locator = (By.CSS_SELECTOR, 'body.loading')
    _next_button_locator = (By.ID, 'email-button')
    _email_input_locator = (By.CSS_SELECTOR, '.email')
    _password_input_locator = (By.ID, 'password')
    _sign_in_button_locator = (By.ID, 'submit-btn')
    _not_you_logout_link_locator = (By.CSS_SELECTOR, '.logout')
    _firefox_logo_locator = (By.ID, 'fox-logo')
    _forgot_password_locator = (By.CSS_SELECTOR, '.left.reset-password')

    def __init__(self, marionette):
        Base.__init__(self, marionette)
        self.switch_to_correct_login_frame()

    def switch_to_correct_login_frame(self):
        self.marionette.switch_to_frame()
        if self.is_element_present(*self._ff_accounts_frame_locator):
            self.switch_login_frame(self._ff_accounts_frame_locator)
        else:
            self.switch_login_frame(self._in_app_login_frame_locator)

    def login(self, email, password):
        self.wait_for_element_displayed(*self._email_input_locator)
        self.type_email(email)
        if self.is_element_present(*self._next_button_locator):
            self.tap_next()
        self.wait_for_element_displayed(*self._password_input_locator)
        self.type_password(password)
        self.tap_sign_in()

    def switch_login_frame(self, locator):
        self.marionette.switch_to_frame()
        self.wait_for_element_present(*locator)
        login_frame = self.marionette.find_element(*locator)
        self.marionette.switch_to_frame(login_frame)
        self.wait_for_element_not_present(*self._body_loading_locator)

    def type_email(self, value):
        email_field = self.marionette.find_element(*self._email_input_locator)
        email_field.send_keys(value)

    def type_password(self, value):
        self.wait_for_element_displayed(*self._password_input_locator)
        password_field = self.marionette.find_element(*self._password_input_locator)
        password_field.send_keys(value)

    def tap_next(self):
        self.marionette.find_element(*self._next_button_locator).tap()

    def tap_sign_in(self):
        self.keyboard.dismiss()
        self.switch_to_correct_login_frame()
        self.wait_for_element_displayed(*self._sign_in_button_locator)
        self.marionette.find_element(*self._sign_in_button_locator).tap()

    @property
    def is_not_you_logout_link_visible(self):
        return self.is_element_displayed(*self._not_you_logout_link_locator)

    def tap_not_you(self):
        self.marionette.find_element(*self._not_you_logout_link_locator).tap()

    def wait_for_password_field_visible(self):
        self.wait_for_element_displayed(*self._password_input_locator)

    @property
    def email_text(self):
        return self.marionette.find_element(*self._email_input_locator).text

    def tap_sign_in(self, second_login=False):
        if not second_login:
            self.keyboard.dismiss()
        self.wait_for_element_displayed(*self._sign_in_button_locator)
        self.marionette.find_element(*self._sign_in_button_locator).tap()

    def tap_forgot_password(self):
        self.marionette.find_element(*self._forgot_password_locator).tap()
