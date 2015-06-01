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

import sqlalchemy as sa
from neutron.db import db_base_plugin_v2 as base_db
from neutron.db import model_base
from neutron.db import models_v2
from neutron.extensions import instantvpn
from neutron.openstack.common import log as logging
from neutron.openstack.common import uuidutils


LOG = logging.getLogger(__name__)

class InstantvpnDbMixin(instantvpn.InstantvpnPluginBase,
                      base_db.CommonDbMixin):
    """Mixin class for InstantVpn DB implementation."""
    
    def _make_instantvpn_dict(self, instantvpn, fields=None):
        res = {'name': instantvpn['name'],
               'tenant_id': instantvpn['tenant_id']}
        return self._fields(res, fields)

    def create_instantvpn(self, context, instantvpn):
        m = instantvpn['instantvpn']
        tenant_id = self._get_tenant_id_for_create(context, m)

        with context.session.begin(subtransactions=True):
            instantvpn_db = Instantvpn(id=uuidutils.generate_uuid(),
                                     tenant_id=tenant_id,
                                     name=m['name'])
            context.session.add(instantvpn_db)

        return self._make_instantvpn_dict(instantvpn_db)

    def delete_instantvpn(self, context, vpn_name):
        pass

    def get_instantvpns(self, context, filters=None, fields=None,
                            sorts=None, limit=None, marker=None,
                            page_reverse=False):
        marker_obj = self._get_marker_obj(context, 'instantvpns', limit,
                                          marker)
        return self._get_collection(context, Instantvpn,
                                    self._make_instantvpn_dict,
                                    filters=filters, fields=fields,
                                    sorts=sorts,
                                    limit=limit,
                                    marker_obj=marker_obj,
                                    page_reverse=page_reverse)

class Instantvpn(model_base.BASEV2, models_v2.HasId, models_v2.HasTenant):
    """Represents a InstantVpn resource."""
    name = sa.Column(sa.String(255))