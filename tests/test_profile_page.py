#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
import random
import string
from copy import deepcopy
from unittestzero import Assert

from pages.home import Home


class TestProfilePage:

    @pytest.mark.credentials
    def test_edit_profile_fields(self, mozwebqa):
        home_page = Home(mozwebqa)
        home_page.login()

        profile_page = home_page.header.click_profile()
        user_edit_page = profile_page.click_edit_profile()
        Assert.true(user_edit_page.is_the_current_page)

        # save initial values to restore them after the test is finished
        fields_no = len(user_edit_page.profile_fields)
        initial_value = [None] * fields_no
        random_name = "test%s" % random.choice(string.lowercase)

        # enter new values
        for i in range(0, fields_no):
            initial_value[i] = deepcopy(user_edit_page.profile_fields[i].field_value)
            user_edit_page.profile_fields[i].clear_field()
            user_edit_page.profile_fields[i].type_value(random_name)

        user_edit_page.click_save_profile()
        Assert.true(profile_page.is_update_message_visible)
        profile_page.click_edit_profile()

        # using try finally to ensure that the initial values are restore even if the Asserts fail.
        try:
            for i in range(0, fields_no):
                Assert.contains(random_name, user_edit_page.profile_fields[i].field_value)

        except Exception as exception:
            Assert.fail(exception)

        finally:
            # go back and restore initial values
            for i in range(0, fields_no):
                user_edit_page.profile_fields[i].clear_field()
                user_edit_page.profile_fields[i].type_value(initial_value[i])

            user_edit_page.click_save_profile()

    @pytest.mark.credentials
    def test_user_can_create_and_delete_report(self, mozwebqa):
        test_link = 'http://test.com'
        random_text = "test%s" % random.choice(string.lowercase)

        home_page = Home(mozwebqa)
        home_page.login()

        dashboard = home_page.header.click_dashboard()
        new_report = dashboard.click_add_new_report()
        new_report.select_activity('3')
        new_report.select_campaign('1')
        new_report.select_contribution_area('Coding')
        new_report.select_event_place()
        new_report.type_url_for_activity(test_link)
        new_report.type_url_description(random_text)
        new_report.type_activity_description(random_text)
        view_report = new_report.click_save_report_button()
        Assert.true(view_report.is_success_message_visible)
        Assert.contains('Report successfully created.', view_report.success_message_text)
        edit_report = view_report.click_edit_report()
        view_report = edit_report.delete_report()
        Assert.true(view_report.is_success_message_visible)
        Assert.contains('Report successfully deleted.', view_report.success_message_text)
