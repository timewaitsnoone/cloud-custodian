# Copyright The Cloud Custodian Authors.
# SPDX-License-Identifier: Apache-2.0

import logging
import os
import sys

from huaweicloudsdkconfig.v1 import ConfigClient, ShowTrackerConfigRequest
from huaweicloudsdkconfig.v1.region.config_region import ConfigRegion
from huaweicloudsdkcore.auth.credentials import BasicCredentials, GlobalCredentials
from huaweicloudsdkecs.v2 import EcsClient
from huaweicloudsdkecs.v2.region.ecs_region import EcsRegion
from huaweicloudsdkevs.v2 import EvsClient, ListVolumesRequest
from huaweicloudsdkevs.v2.region.evs_region import EvsRegion
from huaweicloudsdkiam.v3 import IamClient
from huaweicloudsdkiam.v3.region.iam_region import IamRegion
from huaweicloudsdkvpc.v2 import ListSecurityGroupsRequest
from huaweicloudsdkvpc.v2.vpc_client import VpcClient as VpcClientV2
from huaweicloudsdkvpc.v3.region.vpc_region import VpcRegion
from huaweicloudsdkvpc.v3.vpc_client import VpcClient as VpcClientV3
from huaweicloudsdkfunctiongraph.v2 import FunctionGraphClient, ListFunctionsRequest
from huaweicloudsdkfunctiongraph.v2.region.functiongraph_region import FunctionGraphRegion
from huaweicloudsdktms.v1 import TmsClient
from huaweicloudsdktms.v1.region.tms_region import TmsRegion
from huaweicloudsdkdeh.v1 import DeHClient, ListDedicatedHostsRequest
from huaweicloudsdkdeh.v1.region.deh_region import DeHRegion
from huaweicloudsdkces.v2 import CesClient, ListAlarmRulesRequest
from huaweicloudsdkces.v2.region.ces_region import CesRegion
from huaweicloudsdksmn.v2 import SmnClient
from huaweicloudsdksmn.v2.region.smn_region import SmnRegion
from huaweicloudsdkorganizations.v1 import *
from huaweicloudsdkorganizations.v1.region.organizations_region import OrganizationsRegion
from huaweicloudsdkeg.v1 import EgClient
from huaweicloudsdkeg.v1.region.eg_region import EgRegion


log = logging.getLogger('custodian.huaweicloud.client')


class Session:
    """Session"""

    def __init__(self, options=None):
        self.region = os.getenv('HUAWEI_DEFAULT_REGION')
        self.token = None
        if not self.region:
            log.error('No default region set. Specify a default via HUAWEI_DEFAULT_REGION')
            sys.exit(1)

        if options is not None:
            self.ak = options.get('SecurityAccessKey')
            self.sk = options.get('SecuritySecretKey')
            self.token = options.get('SecurityToken')
        self.ak = os.getenv('HUAWEI_ACCESS_KEY_ID') or self.ak
        if self.ak is None:
            log.error('No access key id set. '
                      'Specify a default via HUAWEI_ACCESS_KEY_ID or context')
            sys.exit(1)

        self.sk = os.getenv('HUAWEI_SECRET_ACCESS_KEY') or self.sk
        if self.sk is None:
            log.error('No secret access key set. '
                      'Specify a default via HUAWEI_SECRET_ACCESS_KEY or context')
            sys.exit(1)

        self.tms_region = os.getenv('HUAWEI_DEFAULT_TMS_REGION')
        if not self.tms_region:
            self.tms_region = 'cn-north-4'

    def client(self, service):
        credentials = BasicCredentials(self.ak, self.sk, os.getenv('HUAWEI_PROJECT_ID')) \
            .with_security_token(self.token)
        if service == 'vpc':
            client = VpcClientV3.new_builder() \
                .with_credentials(credentials) \
                .with_region(VpcRegion.value_of(self.region)) \
                .build()
        elif service == 'vpc_v2':
            client = VpcClientV2.new_builder() \
                .with_credentials(credentials) \
                .with_region(VpcRegion.value_of(self.region)) \
                .build()
        elif service == 'ecs':
            client = EcsClient.new_builder() \
                .with_credentials(credentials) \
                .with_region(EcsRegion.value_of(self.region)) \
                .build()
        elif service == 'evs':
            client = EvsClient.new_builder() \
                .with_credentials(credentials) \
                .with_region(EvsRegion.value_of(self.region)) \
                .build()
        elif service == 'tms':
            globalCredentials = GlobalCredentials(self.ak, self.sk)
            client = TmsClient.new_builder() \
                .with_credentials(globalCredentials) \
                .with_region(TmsRegion.value_of(self.tms_region)) \
                .build()
        elif service == 'iam':
            globalCredentials = GlobalCredentials(self.ak, self.sk)
            client = IamClient.new_builder() \
                .with_credentials(globalCredentials) \
                .with_region(IamRegion.value_of(self.region)) \
                .build()
        elif service == 'config':
            globalCredentials = GlobalCredentials(self.ak, self.sk)
            client = ConfigClient.new_builder() \
                .with_credentials(globalCredentials) \
                .with_region(ConfigRegion.value_of(self.region)) \
                .build()
        elif service == 'deh':
            client = DeHClient.new_builder() \
                .with_credentials(credentials) \
                .with_region(DeHRegion.value_of(self.region)) \
                .build()
        elif service == 'ces':
            client = CesClient.new_builder() \
                .with_credentials(credentials) \
                .with_region(CesRegion.value_of(self.region)) \
                .build()
        elif service == 'smn':
            client = SmnClient.new_builder() \
                .with_credentials(credentials) \
                .with_region(SmnRegion.value_of(self.region)) \
                .build()
        elif service in ['org-policy','org-unit','org-account']:
            globalCredentials = GlobalCredentials(self.ak, self.sk)
            client = OrganizationsClient.new_builder() \
                .with_credentials(globalCredentials) \
                .with_region(OrganizationsRegion.value_of(self.region)) \
                .build()    
        elif service == 'functiongraph':
            client = FunctionGraphClient.new_builder() \
                .with_credentials(credentials) \
                .with_region(FunctionGraphRegion.value_of(self.region)) \
                .build()
        elif service == 'eg':
            client = EgClient.new_builder() \
                .with_credentials(credentials) \
                .with_region(EgRegion.value_of(self.region)) \
                .build()

        return client

    def request(self, service):
        if service == 'vpc' or service == 'vpc_v2':
            request = ListSecurityGroupsRequest()
        elif service == 'evs':
            request = ListVolumesRequest()
        elif service == 'config':
            request = ShowTrackerConfigRequest()
        elif service == 'deh':
            request = ListDedicatedHostsRequest()
        elif service == 'ces':
            request = ListAlarmRulesRequest()        
        elif service == 'org-policy':
            request = ListPoliciesRequest()
        elif service == 'org-unit':
            request = ListOrganizationalUnitsRequest()
        elif service == 'org-account':
            request = ListAccountsRequest()
        elif service == 'functiongraph':
            request = ListFunctionsRequest()

        return request
