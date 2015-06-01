# Copyright 2013 Big Switch Networks, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import abc

import six

from neutron.api import extensions
from neutron.api.v2 import attributes as attr
from neutron.api.v2 import resource_helper
from neutron.common import exceptions as qexception
from neutron.openstack.common import log as logging
from neutron.plugins.common import constants
from neutron.services import service_base


LOG = logging.getLogger(__name__)

RESOURCE_ATTRIBUTE_MAP = {
        'instantvpns': {
        'name': {'allow_post': True, 'allow_put': True,
                     'is_visible': True},
        # tenant_id is the user id used by keystone for authorisation
        # It's good to use the following as it is and it is necessary
        # for every extension 
        'tenant_id': {'allow_post': True, 'allow_put': False,
                      'required_by_policy': True,
                      'validate': {'type:string': None},
                      'is_visible': True}
        }
    }

class Instantvpn(extensions.ExtensionDescriptor):
    # The name of this class should be the same as the file name
    # There are a couple of methods and their properties defined in the
    # parent class of this class, ExtensionDescriptor you can check them

    @classmethod
    def get_name(cls):
        # You can coin a name for this extension
        return "instantvpn service"

    @classmethod
    def get_alias(cls):
        # This alias will be used by your core_plugin class to load
        # the extension
        return "instantvpn"

    @classmethod
    def get_description(cls):
        # A small description about this extension
        return "Extension for instantvpn service"

    @classmethod
    def get_namespace(cls):
        # The XML namespace for this extension
        # but as we move on to use JSON over XML based request
        # this is not that important, correct me if I am wrong.
        return "http://wiki.openstack.org/Neutron/FWaaS/API_1.0"

    @classmethod
    def get_updated(cls):
        # Specify when was this extension last updated,
        # good for management when there are changes in the design
        return "2014-05-06T10:00:00-00:00"

    @classmethod
    def get_resources(cls):
        """Returns Ext Resources."""
        plural_mappings = resource_helper.build_plural_mappings(
            {}, RESOURCE_ATTRIBUTE_MAP)
        attr.PLURALS.update(plural_mappings)
        return resource_helper.build_resource_info(plural_mappings,
                                                   RESOURCE_ATTRIBUTE_MAP,
                                                   constants.INSTANTVPN,
                                                   translate_name=True,
                                                   allow_bulk=True)    
@six.add_metaclass(abc.ABCMeta)
class InstantvpnPluginBase(service_base.ServicePluginBase):

    def get_plugin_name(self):
        return constants.INSTANTVPN

    def get_plugin_type(self):
        return constants.INSTANTVPN

    def get_plugin_description(self):
        return 'INSTANTVPN service plugin'

    @abc.abstractmethod
    def get_instantvpns(self, context, filters=None, fields=None):
        pass
    
    @abc.abstractmethod
    def create_instantvpn(self, context, instantvpn):
        pass

    @abc.abstractmethod
    def delete_instantvpn(self, context, idx):
        pass

class InstantvpnInternalDriverError(qexception.NeutronException):
    """InstantVpn exception for all driver errors.

    On any failure or exception in the driver, driver should log it and
    raise this exception to the agent
    """
    message = _("%(driver)s: Internal driver error.")