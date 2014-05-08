# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marketplacetests.marketplace_gaia_test import MarketplaceGaiaTestCase
from marketplacetests.marketplace.app import Marketplace
from gaiatest.mocks.persona_test_user import PersonaTestUser


class TestMarketplaceFeedback(MarketplaceGaiaTestCase):
    MARKETPLACE_DEV_NAME = 'Marketplace Dev'
    feedback_submitted_message = u'Feedback submitted. Thanks!'
    test_comment = 'This is a test comment.'

    def test_marketplace_feedback_user(self):
        # launch marketplace dev and go to marketplace
        marketplace = Marketplace(self.marionette, self.MARKETPLACE_DEV_NAME)
        marketplace.launch()
        marketplace.wait_for_page_to_load()

        user = PersonaTestUser().create_user(verified=True,
                                             env={"browserid": "firefoxos.persona.org", "verifier": "marketplace-dev.allizom.org"})
        marketplace.login(user)

        # go to feedback tab
        marketplace.select_setting_feedback()

        # enter and submit your feedback
        marketplace.enter_feedback(self.test_comment)
        marketplace.submit_feedback()

        # catch the notification
        marketplace.wait_for_notification_message_displayed()
        message_content = marketplace.notification_message

        # verify if the notification is right
        self.assertEqual(message_content, self.feedback_submitted_message)
