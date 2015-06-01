# Copyright (C) 2013 eNovance SAS <licensing@enovance.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from neutron.db.instantvpn import instantvpn_db
from neutron.openstack.common import log as logging
from neutron.services.instantvpn.driver import instantvpn_smtpdriver as driver

LOG = logging.getLogger(__name__)

class InstantVpnPlugin(instantvpn_db.InstantvpnDbMixin):
    """Implementation of the Neutron InstantVpn Service Plugin.

    This class manages the workflow of InstantVpn request/response.
    Most DB related works are implemented in class
    instantvpn_db.InstantvpnDbMixin.
    """
    supported_extension_aliases = ["instantvpn"]

    def __init__(self):
        super(InstantVpnPlugin, self).__init__()

    def create_instantvpn(self, context, instantvpn):
        LOG.debug(_("create_instantvpn() called"))
        instantvpn = super(InstantVpnPlugin, self).create_instantvpn(context, instantvpn)
        driver.notify_instantvpn_create(instantvpn)
        return instantvpn

    def delete_instantvpn(self, context, instantvpn):
        LOG.debug(_("delete_instantvpn() called"))
        driver.notify_instantvpn_delete(instantvpn)
