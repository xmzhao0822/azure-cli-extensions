# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import unittest
from unittest import mock

from azext_aimanager import custom
from azext_aimanager.constants import (
    AIMANAGER_CONTRIBUTOR_ROLE,
    AIMANAGER_NAMESPACE_READER_ROLE,
    AIMANAGER_CALLER_ROLES,
    NAMESPACE_CALLER_ROLES,
)


class _FakeResult:
    def __init__(self, resource_id):
        self.id = resource_id


class TestCreateRoleAssignments(unittest.TestCase):
    """Verify create/add commands assign the default caller roles on success."""

    def setUp(self):
        self.cmd = mock.MagicMock()
        self.client = mock.MagicMock()
        # No existing resource so creation proceeds.
        from azure.core.exceptions import ResourceNotFoundError
        self.client.get.side_effect = ResourceNotFoundError("not found")

    def test_default_roles_contain_both_roles(self):
        self.assertEqual(
            AIMANAGER_CALLER_ROLES,
            [AIMANAGER_CONTRIBUTOR_ROLE, AIMANAGER_NAMESPACE_READER_ROLE])

    def test_namespace_roles_contain_reader_only(self):
        self.assertEqual(NAMESPACE_CALLER_ROLES, [AIMANAGER_NAMESPACE_READER_ROLE])
        self.assertNotIn(AIMANAGER_CONTRIBUTOR_ROLE, NAMESPACE_CALLER_ROLES)

    @mock.patch('azext_aimanager.custom.add_caller_role_assignments')
    @mock.patch('azext_aimanager.custom.LongRunningOperation')
    @mock.patch('azext_aimanager.custom._construct_aimanager')
    def test_create_assigns_roles_on_manager_scope(self, mock_construct, mock_lro, mock_assign):
        scope = '/subscriptions/s/resourceGroups/rg/providers/Microsoft.ContainerService/aiManagers/aim'
        mock_lro.return_value.return_value = _FakeResult(scope)

        result = custom.create_aimanager(
            self.cmd, self.client, 'rg', 'aim', location='eastus2')

        self.assertEqual(result.id, scope)
        mock_assign.assert_called_once_with(self.cmd.cli_ctx, scope, AIMANAGER_CALLER_ROLES)

    @mock.patch('azext_aimanager.custom.add_caller_role_assignments')
    @mock.patch('azext_aimanager.custom.LongRunningOperation')
    @mock.patch('azext_aimanager.custom._construct_aimanager')
    def test_create_skips_roles_when_requested(self, mock_construct, mock_lro, mock_assign):
        mock_lro.return_value.return_value = _FakeResult('id')

        custom.create_aimanager(
            self.cmd, self.client, 'rg', 'aim', location='eastus2', skip_role_assignments=True)

        mock_assign.assert_not_called()

    @mock.patch('azext_aimanager.custom.add_caller_role_assignments')
    @mock.patch('azext_aimanager.custom.LongRunningOperation')
    @mock.patch('azext_aimanager.custom._construct_aimanager')
    def test_create_skips_roles_when_no_wait(self, mock_construct, mock_lro, mock_assign):
        custom.create_aimanager(
            self.cmd, self.client, 'rg', 'aim', location='eastus2', no_wait=True)

        mock_assign.assert_not_called()
        mock_lro.assert_not_called()

    @mock.patch('azext_aimanager.custom.add_caller_role_assignments')
    @mock.patch('azext_aimanager.custom.LongRunningOperation')
    @mock.patch('azext_aimanager.custom._construct_namespace')
    def test_namespace_add_assigns_roles_on_namespace_scope(self, mock_construct, mock_lro, mock_assign):
        scope = ('/subscriptions/s/resourceGroups/rg/providers/Microsoft.ContainerService/'
                 'aiManagers/aim/namespaces/ns')
        mock_lro.return_value.return_value = _FakeResult(scope)

        result = custom.add_aimanager_namespace(
            self.cmd, self.client, 'rg', 'aim', 'ns')

        self.assertEqual(result.id, scope)
        mock_assign.assert_called_once_with(self.cmd.cli_ctx, scope, NAMESPACE_CALLER_ROLES)

    @mock.patch('azext_aimanager.custom.add_caller_role_assignments')
    @mock.patch('azext_aimanager.custom.LongRunningOperation')
    @mock.patch('azext_aimanager.custom._construct_namespace')
    def test_namespace_add_skips_roles_when_requested(self, mock_construct, mock_lro, mock_assign):
        mock_lro.return_value.return_value = _FakeResult('id')

        custom.add_aimanager_namespace(
            self.cmd, self.client, 'rg', 'aim', 'ns', skip_role_assignments=True)

        mock_assign.assert_not_called()

    @mock.patch('azext_aimanager.custom.add_caller_role_assignments')
    @mock.patch('azext_aimanager.custom.LongRunningOperation')
    @mock.patch('azext_aimanager.custom._construct_namespace')
    def test_namespace_add_skips_roles_when_no_wait(self, mock_construct, mock_lro, mock_assign):
        custom.add_aimanager_namespace(
            self.cmd, self.client, 'rg', 'aim', 'ns', no_wait=True)

        mock_assign.assert_not_called()
        mock_lro.assert_not_called()


if __name__ == '__main__':
    unittest.main()
