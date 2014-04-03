# -*- coding: UTF-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.by import By
from marionette.marionette import Actions

from gaiatest.apps.keyboard.app import Keyboard


class Keyboard(Keyboard):
    ''' This is a hack to deal with the fact that the version of Keyboard in
        gaiatest v0.21.3, to which we are pinned for v1.3 compatibility
        doesn't work with the PIN entry screen in payments, so this is pulling
        in some methods from Keyboard in master.
    '''

    _keyboards_locator = (By.ID, 'keyboards')
    _keyboard_frame_locator = (By.CSS_SELECTOR, '#keyboards iframe:not([hidden])')
    _button_locator = (By.CSS_SELECTOR, '#keyboard button.keyboard-key[data-keycode="%s"]')

    @property
    def _is_upper_case(self):
        return self.marionette.execute_script('return window.wrappedJSObject.isUpperCase;')

    @property
    def _is_upper_case_locked(self):
        return self.marionette.execute_script('return window.wrappedJSObject.isUpperCaseLocked;')

    @property
    def _current_input_type(self):
        return self.marionette.execute_script('return window.wrappedJSObject.currentInputType;')

    @property
    def _layout_page(self):
        return self.marionette.execute_script('return window.wrappedJSObject.layoutPage;')

    # this is to switch to the frame of keyboard
    def switch_to_keyboard(self):
        self.marionette.switch_to_frame()
        keyboards = self.marionette.find_element(*self._keyboards_locator)
        self.wait_for_condition(lambda m: 'hide' not in keyboards.get_attribute('class') and
                                          not keyboards.get_attribute('data-transition-in'),
                                message="Keyboard not interpreted as displayed. Debug is_displayed(): %s"
                                % keyboards.is_displayed())

        keybframe = self.marionette.find_element(*self._keyboard_frame_locator)
        return self.marionette.switch_to_frame(keybframe, focus=False)

    # this is to get the locator of desired key on keyboard
    def _key_locator(self, val):
        if len(val) == 1:
            val = ord(val)
        return (self._button_locator[0], self._button_locator[1] % val)

    # this is to tap on desired key on keyboard
    def _tap(self, val):
        is_upper_case = self._is_upper_case
        is_upper_case_locked = self._is_upper_case_locked

        self.wait_for_element_displayed(*self._key_locator(val))
        key = self.marionette.find_element(*self._key_locator(val))
        Actions(self.marionette).press(key).wait(0.1).release().perform()

        # These two tap cases are most important because they cause the keyboard to change state which affects next step
        if val.isspace():
            # Space switches back to Default layout
            self.wait_for_condition(lambda m: self._layout_page == 'Default')
        if val.isupper() and is_upper_case and not is_upper_case_locked:
            # Tapping key with shift enabled causes the keyboard to switch back to lower
            self.wait_for_condition(lambda m: not self._is_upper_case)
