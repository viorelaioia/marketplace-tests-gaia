# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.by import By
from gaiatest.apps.base import Base

from marketplacetests.keyboard.app import Keyboard


class Payment(Base):

    _payment_frame_locator = (By.CSS_SELECTOR, "#trustedui-frame-container > iframe")

    # Create/confirm PIN
    _create_pin_form_locator = (By.CSS_SELECTOR, 'form[action="/mozpay/pin/create"]')
    _pin_input_locator = (By.CSS_SELECTOR, 'div.pinbox span')
    _confirm_pin_form_locator = (By.CSS_SELECTOR, 'form[action="/mozpay/pin/confirm"]')
    _pin_continue_button_locator = (By.CSS_SELECTOR, '#pin > footer > button')

    # Final buy app panel
    _app_name_locator = (By.CSS_SELECTOR, '.product .title')
    _buy_button_locator = (By.XPATH, "//button[text()='Buy']")
    _cancel_button_locator = (By.XPATH, "//button[text()='Cancel']")

    def __init__(self, marionette):
        Base.__init__(self, marionette)
        self.switch_to_payment_frame()

    def switch_to_payment_frame(self):
        self.marionette.switch_to_frame()
        self.wait_for_element_present(*self._payment_frame_locator)
        payment_iframe = self.marionette.find_element(*self._payment_frame_locator)
        self.marionette.switch_to_frame(payment_iframe)

    @property
    def app_name(self):
        return self.marionette.find_element(*self._app_name_locator).text

    def create_pin(self, pin):
        self.wait_for_element_displayed(*self._create_pin_form_locator)
        self.type_pin_number(pin)
        self.tap_pin_continue()
        self.wait_for_element_displayed(*self._confirm_pin_form_locator)
        self.type_pin_number(pin)
        self.tap_pin_continue()

    def type_pin_number(self, pin):
        keyboard = Keyboard(self.marionette)
        self.marionette.find_element(*self._pin_input_locator).tap()
        keyboard.switch_to_keyboard()
        for num in pin:
            keyboard._tap(num)
        self.switch_to_payment_frame()

    def tap_pin_continue(self):
        self.marionette.find_element(*self._pin_continue_button_locator).tap()

    def wait_for_buy_app_section_displayed(self):
        self.wait_for_element_displayed(*self._buy_button_locator)

    def tap_buy_button(self):
        self.marionette.find_element(*self._buy_button_locator).tap()
        self.marionette.switch_to_frame()
        self.wait_for_element_not_present(*self._payment_frame_locator)
        self.marionette.switch_to_frame()
