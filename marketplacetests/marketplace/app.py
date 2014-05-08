# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.by import By
from marionette.keys import Keys
from gaiatest.apps.base import Base


class Marketplace(Base):

    # Default to the Dev app
    name = 'Marketplace Dev'

    _marketplace_iframe_locator = (By.CSS_SELECTOR, 'iframe[src*="marketplace"]')

    _gallery_apps_locator = (By.CSS_SELECTOR, '#gallery .app')
    _loading_fragment_locator = (By.CSS_SELECTOR, 'div.loading-fragment')
    _error_title_locator = (By.CSS_SELECTOR, 'h1.title')
    _error_message_locator = (By.CSS_SELECTOR, 'span.message')
    _settings_button_locator = (By.CSS_SELECTOR, 'a.header-button.settings')
    _home_button_locator = (By.CSS_SELECTOR, 'h1.site a')
    _back_button_locator = (By.ID, 'nav-back')
    _notification_locator = (By.ID, 'notification-content')
    _popular_apps_tab_locator = (By.CSS_SELECTOR, '#gallery .tabs a:nth-child(1)')
    _featured_section_locator = (By.ID, 'featured')

    # Marketplace settings tabs
    _account_tab_locator = (By.CSS_SELECTOR, 'a[href="/settings"]')
    _my_apps_tab_locator = (By.CSS_SELECTOR, 'a[href="/purchases"]')
    _feedback_tab_locator = (By.CSS_SELECTOR, 'a[href="/feedback"]')
    _feedback_textarea_locator = (By.NAME, 'feedback')
    _feedback_submit_button_locator = (By.CSS_SELECTOR, 'button[type="submit"]')

    # Marketplace search on home page
    _search_locator = (By.ID, 'search-q')
    _signed_in_notification_locator = (By.CSS_SELECTOR, '#notification.show')

    # System app install notification message
    _install_notification_locator = (By.CSS_SELECTOR, '#system-banner > p')

    def __init__(self, marionette, app_name=False):
        Base.__init__(self, marionette)
        if app_name:
            self.name = app_name

    def launch(self):
        Base.launch(self, launch_timeout=210000)

    def wait_for_page_to_load(self):
        self.wait_for_element_not_present(*self._loading_fragment_locator)
        self.wait_for_element_displayed(*self._featured_section_locator)

    def login(self, user):

        settings = self.tap_settings()
        persona = settings.tap_sign_in()
        persona.login(user.email, user.password)
        self.marionette.switch_to_frame()
        self.launch()
        settings.wait_for_sign_out_button()
        self.wait_for_notification_message_not_displayed()
        return settings

    @property
    def error_title_text(self):
        return self.marionette.find_element(*self._error_title_locator).text

    @property
    def error_message_text(self):
        return self.marionette.find_element(*self._error_message_locator).text

    def wait_for_notification_message_displayed(self):
        self.wait_for_element_displayed(*self._notification_locator)

    def wait_for_notification_message_not_displayed(self):
        self.wait_for_element_not_displayed(*self._notification_locator)

    @property
    def notification_message(self):
        return self.marionette.find_element(*self._notification_locator).text

    @property
    def popular_apps(self):
        self.show_popular_apps()
        from marketplacetests.marketplace.regions.search_results import Result
        return [Result(self.marionette, app) for app in self.marionette.find_elements(*self._gallery_apps_locator)]

    def search(self, term):
        search_box = self.marionette.find_element(*self._search_locator)

        # search for the app
        search_box.send_keys(term)

        search_box.send_keys(Keys.RETURN)
        from marketplacetests.marketplace.regions.search_results import SearchResults
        return SearchResults(self.marionette)

    def set_region(self, region):
        # go to the :debug page
        search_box = self.marionette.find_element(*self._search_locator)
        search_box.send_keys(':debug')
        search_box.send_keys(Keys.RETURN)

        from marketplacetests.marketplace.regions.debug import Debug
        debug_screen = Debug(self.marionette)
        debug_screen.select_region(region)
        # wait for notification of the change
        self.wait_for_notification_message_displayed()
        if region not in self.notification_message:
            raise Exception('Unable to change region to %s. Notification displayed: %s'
                            % (region, self.notification_message))

        debug_screen.tap_back()

    def navigate_to_app(self, app_name):
        search_results = self.search(app_name).search_results
        for result in search_results:
            if result.name == app_name:
                return result.tap_app()

        # app not found
        raise Exception('The app: %s was not found.' % app_name)

    def show_popular_apps(self):
        self.marionette.find_element(*self._popular_apps_tab_locator).tap()
        self.wait_for_condition(lambda m: 'active' in m.find_element(*self._popular_apps_tab_locator).get_attribute('class'))

    def tap_settings(self):
        self.wait_for_element_displayed(*self._settings_button_locator)
        self.marionette.find_element(*self._settings_button_locator).tap()
        from marketplacetests.marketplace.regions.settings import Settings
        return Settings(self.marionette)

    def tap_home(self):
        self.marionette.find_element(*self._home_button_locator).tap()

    def tap_back(self):
        self.marionette.find_element(*self._back_button_locator).tap()

    def select_setting_account(self):
        self.marionette.find_element(*self._account_tab_locator).tap()

    def select_setting_my_apps(self):
        self.marionette.find_element(*self._my_apps_tab_locator).tap()

    def select_setting_feedback(self):
        self.marionette.find_element(*self._feedback_tab_locator).tap()

    def enter_feedback(self, feedback_text):
        feedback = self.marionette.find_element(*self._feedback_textarea_locator)
        feedback.clear()
        feedback.send_keys(feedback_text)
        self.keyboard.dismiss()

    def submit_feedback(self):
        self.wait_for_element_displayed(*self._feedback_submit_button_locator)
        self.marionette.find_element(*self._feedback_submit_button_locator).tap()

    @property
    def install_notification_message(self):
        self.marionette.switch_to_frame()
        self.wait_for_element_displayed(*self._install_notification_locator)
        return self.marionette.find_element(*self._install_notification_locator).text
