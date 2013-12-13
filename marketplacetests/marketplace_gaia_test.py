# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest.gaia_test import GaiaTestCase
from marionette.by import By


class MarketplaceGaiaTestCase(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.connect_to_network()
        self.install_marketplace()

    def install_marketplace(self):
        _yes_button_locator = (By.ID, 'app-install-install-button')

        if not self.apps.is_app_installed('Marketplace Dev'):
            # install the marketplace dev app
            self.marionette.execute_script('navigator.mozApps.install("https://marketplace-dev.allizom.org/manifest.webapp")')

            # TODO add this to the system app object when we have one
            self.wait_for_element_displayed(*_yes_button_locator)
            self.marionette.find_element(*_yes_button_locator).tap()
            self.wait_for_element_not_displayed(*_yes_button_locator)
