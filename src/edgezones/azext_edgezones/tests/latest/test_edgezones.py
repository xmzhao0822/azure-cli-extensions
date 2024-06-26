# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#
# Code generated by aaz-dev-tools
# --------------------------------------------------------------------------------------------

from azure.cli.testsdk import *


class EdgezonesScenario(ScenarioTest):
    # TODO: add tests here
    def test_list_extended_zones(self):
        extendedzones_list = self.cmd('az edge-zones extended-zone list').get_output_in_json()
        assert len(extendedzones_list) > 0

    def test_show_extended_zone(self):
        self.kwargs.update({
            'name': 'losangeles'
        })
        self.cmd('az edge-zones extended-zone show --extended-zone-name {name}', checks=[
            self.check('name', '{name}')    
        ])
        
    def test_register_extended_zone(self):
        self.kwargs.update({
            'name': 'losangeles'
        })
        self.cmd('az edge-zones extended-zone register --extended-zone-name {name}', checks=[
            self.check('name', '{name}'),
            self.check('registrationState', 'Registered')
        ])
        
    def test_unregister_extended_zone(self):
        self.kwargs.update({
            'name': 'microsoftrrezm1'
        })
        self.cmd('az edge-zones extended-zone unregister --extended-zone-name {name}', checks=[
            self.check('name', '{name}'),
            self.check('registrationState', 'NotRegistered')
        ])
    pass
