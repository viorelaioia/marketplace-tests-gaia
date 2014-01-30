# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os

from gaiatest.gaia_test import GaiaTestCase
from marionette.by import By


class MarketplaceGaiaTestCase(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.install_certs()
        self.connect_to_network()
        self.install_marketplace()

    def install_certs(self):
        """ Install the marketplace-dev certs and set the pref required """
        certs_folder = os.path.join('marketplacetests', 'certs')
        for file_name in self.device.manager.listFiles('/data/b2g/mozilla/'):
            if file_name.endswith('.default'):
                profile_folder = file_name
                break
        for file_name in os.listdir(certs_folder):
            self.device.push_file(os.path.join(certs_folder, file_name),
                                  destination='data/b2g/mozilla/%s/%s' % (profile_folder, file_name))
        self.data_layer.set_char_pref('dom.mozApps.signed_apps_installable_from',
                                      'https://marketplace-dev.allizom.org,https://marketplace.firefox.com')

    def install_marketplace(self):
        _yes_button_locator = (By.ID, 'app-install-install-button')

        if not self.apps.is_app_installed('Marketplace Dev'):
            # install the marketplace dev app
            self.marionette.execute_script('navigator.mozApps.install("https://marketplace-dev.allizom.org/manifest.webapp")')

            # TODO add this to the system app object when we have one
            self.wait_for_element_displayed(*_yes_button_locator)
            self.marionette.find_element(*_yes_button_locator).tap()
            self.wait_for_element_not_displayed(*_yes_button_locator)
