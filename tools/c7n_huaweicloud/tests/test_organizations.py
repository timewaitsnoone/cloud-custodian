# Copyright The Cloud Custodian Authors.
# SPDX-License-Identifier: Apache-2.0
import os
from huaweicloud_common import BaseTest

os.environ['HUAWEI_DEFAULT_REGION'] = 'cn-north-4'

class OrganizationsTest(BaseTest):

    def test_list_account(self):
        factory = self.replay_flight_data('organizations/list_account')
        p = self.load_policy({
            "name": "list-org-account",
            "resource": "huaweicloud.org-account",
            "filters": [{
                "type": "value",
                "key": "status",
                "value": "active"
            }]
        }, session_factory=factory)
        resources = p.run()
        self.assertEqual(len(resources), 2)
        self.assertEqual(resources[0]['name'], "fake_account_naem")
        self.assertEqual(resources[0]['id'], "8e5fe930d666666666666666602c")
        
    def test_list_policy(self):
        factory = self.replay_flight_data('organizations/list_policy')
        p = self.load_policy({
            "name": "list-org-policy",
            "resource": "huaweicloud.org-policy",
            "filters": [{
                "type": "value",
                "key": "type",
                "value": "service_control_policy"
            }]
        }, session_factory=factory)
        resources = p.run()
        self.assertEqual(len(resources), 1)
        self.assertEqual(resources[0]['name'], "RestrictedForOU1")
        self.assertEqual(resources[0]['id'], "p-27lu7qg666666666666bm9jzk2zzk0")

    def test_list_unit(self):
        factory = self.replay_flight_data('organizations/list_unit')
        p = self.load_policy({
            "name": "list-org-unit",
            "resource": "huaweicloud.org-unit",
            "filters": [{
                "type": "value",
                "key": "id",
                "value": "^ou-[0-9a-z]{8,32}$",
                "op": "regex"
            }]
        }, session_factory=factory)
        resources = p.run()
        self.assertEqual(len(resources), 2)
        self.assertEqual(resources[0]['name'], "RestrictedForOU1")
        self.assertEqual(resources[0]['id'], "p-27lu7qg666666666666bm9jzk2zzk0")