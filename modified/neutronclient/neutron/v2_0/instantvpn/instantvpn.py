# Copyright 2013 Big Switch Networks
# All Rights Reserved
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
#
# @author: KC Wang, Big Switch Networks
#

import argparse

from neutronclient.i18n import _
from neutronclient.neutron import v2_0 as neutronv20


class ListInstantVpn(neutronv20.ListCommand):
    """List instantvpns that belong to a given tenant."""

    resource = 'instantvpn'
    list_columns = ['name']
    _formatters = {}
    pagination_support = True
    sorting_support = True

class CreateInstantVpn(neutronv20.CreateCommand):
    """Create a InstantVpn."""
    # This class will forward to the create_instantvpn method of your
    # neutron plugin. This will go in as a dictionary which your plugin
    # to process.
    
    resource = 'instantvpn'

    def add_known_arguments(self, parser):
        # This method is used to define the arguments that this CLI
        # command expects. Our InstantVpn extensions allows users to
        # specify vpnname credential. When a user hits
        # "neutron instantvpn-create --help", information from these are
        # displayed.
        
        parser.add_argument(
            '--name',
            help=_('Instance VPN name.'))
        
        # Sample usage:
        # neutron instantvpn-create vpn1
        # Here, name is vpn1
    
    def args2body(self, parsed_args):
        # This method will create a dictionary of all the specified arguments
        # and forward this data to the next step in neutronclient
        body = {'instantvpn': {
                    'name': parsed_args.name,
               }}
 
        if parsed_args.tenant_id:
            # this way can be used to check if the attribute has been specified
            # in the CLI. Default values need not be given here if user has
            # not specified the attribute as the "default" key in the extensions
            # dictionary will fill for absent attributes.
            body['instantvpn'].update({'tenant_id': parsed_args.tenant_id})
 
        return body

class DeleteInstantVpn(neutronv20.DeleteCommand):
    """Delete a given InstantVpn."""

    resource = 'instantvpn'
    
