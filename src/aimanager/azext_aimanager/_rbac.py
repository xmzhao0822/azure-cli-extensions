# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import time
import uuid

from azure.cli.core.azclierror import CLIInternalError
from azure.cli.core.commands.arm import resolve_role_id
from azure.cli.core.commands.client_factory import get_mgmt_service_client
from azure.mgmt.authorization import AuthorizationManagementClient
from azure.mgmt.authorization.models import PrincipalType, RoleAssignmentCreateParameters
from azure.core.exceptions import HttpResponseError, ResourceExistsError
from knack.log import get_logger

logger = get_logger(__name__)


def _gen_guid():
    return uuid.uuid4()


def _get_login_account_principal_id(cli_ctx):
    from azure.cli.core._profile import (  # pylint: disable=protected-access
        Profile,
        _SERVICE_PRINCIPAL,
        _USER_ENTITY,
        _USER_NAME,
        _USER_TYPE,
    )
    from azure.cli.command_modules.role import graph_client_factory

    profile = Profile(cli_ctx=cli_ctx)
    active_account = profile.get_subscription()
    assignee = active_account[_USER_ENTITY][_USER_NAME]

    graph_client = graph_client_factory(cli_ctx)
    try:
        if active_account[_USER_ENTITY][_USER_TYPE] == _SERVICE_PRINCIPAL:
            result = list(graph_client.service_principal_list(
                filter=f"servicePrincipalNames/any(c:c eq '{assignee}')"))
        else:
            result = [graph_client.signed_in_user_get()]
    except Exception as error:  # pylint: disable=broad-except
        raise CLIInternalError(f"Failed to get the current logged-in account. {error}")
    if not result:
        raise CLIInternalError(
            f"Failed to retrieve the principal id for '{assignee}', which is needed to create the "
            "default role assignments.")
    return result[0]['id']


def _create_role_assignment(cli_ctx, principal_id, role_definition_id, scope):
    assignments_client = get_mgmt_service_client(cli_ctx, AuthorizationManagementClient).role_assignments
    principal_types = [p.value for p in PrincipalType]
    current_principal_type = principal_types.pop(0)

    logger.info("Creating a role assignment with role '%s' on the scope of '%s'", role_definition_id, scope)
    retry_times = 36
    assignment_name = _gen_guid()
    for retry_time in range(0, retry_times):
        try:
            parameters = RoleAssignmentCreateParameters(
                role_definition_id=role_definition_id,
                principal_id=principal_id,
                principal_type=current_principal_type)
            assignments_client.create(
                scope=scope, role_assignment_name=assignment_name, parameters=parameters)
            break
        except ResourceExistsError:
            logger.info('Role assignment already exists')
            break
        except HttpResponseError as ex:
            if 'UnmatchedPrincipalType' in (ex.message or ''):
                logger.debug("Principal type '%s' is not matched", current_principal_type)
                try:
                    current_principal_type = principal_types.pop(0)
                except IndexError:
                    raise CLIInternalError(
                        "Failed to create a role assignment. No matching principal types found.")
                continue
            if 'role assignment already exists' in (ex.message or '').lower():
                logger.info('Role assignment already exists')
                break
            if retry_time < retry_times - 1 and ' does not exist in the directory ' in (ex.message or '').lower():
                time.sleep(5)
                logger.warning('Retrying role assignment creation: %s/%s', retry_time + 1, retry_times)
                continue
            raise


def add_caller_role_assignments(cli_ctx, scope, role_names):
    """Assign the given built-in roles to the current CLI caller on the provided resource scope.

    Failures are logged as warnings rather than raised so that a successful create/add operation
    is not reported as a failure when the caller lacks permission to manage role assignments.
    """
    subscription_id = get_mgmt_service_client(
        cli_ctx, AuthorizationManagementClient)._config.subscription_id  # pylint: disable=protected-access
    subscription_scope = '/subscriptions/' + subscription_id

    try:
        principal_id = _get_login_account_principal_id(cli_ctx)
    except CLIInternalError as ex:
        logger.warning(
            "Skipping default role assignments because the caller principal id could not be resolved: %s", ex)
        return

    for role_name in role_names:
        try:
            role_definition_id = resolve_role_id(cli_ctx, role_name, subscription_scope)
            _create_role_assignment(cli_ctx, principal_id, role_definition_id, scope)
        except Exception as ex:  # pylint: disable=broad-except
            logger.warning(
                "Failed to assign role '%s' to the caller on scope '%s'. You may need to create this "
                "role assignment manually. Error: %s", role_name, scope, ex)
