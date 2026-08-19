# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# Delete policy values for an AI Manager resource.
DELETE_POLICY_KEEP = "Keep"
DELETE_POLICY_DELETE = "Delete"
DELETE_POLICIES = [DELETE_POLICY_KEEP, DELETE_POLICY_DELETE]

MODEL_DEPLOYMENT_PERFORMANCE_MODES = ["Balanced", "Latency", "Throughput"]

# Table output projections for the 'az aimanager model' commands.
AI_MODEL_TABLE_TRANSFORMER = (
    "[].{Name:name, ModelId:properties.modelId, Description:properties.description}"
)

CALCULATE_COST_TABLE_TRANSFORMER = (
    "plans[].{VmSize:vmSize, Feasible:feasible, VmsPerReplica:vmsPerReplica, "
    "VmHourlyPrice:vmHourlyPrice, TotalHourlyPrice:totalHourlyPrice, "
    "MaxAvailableReplicas:maxAvailableReplicas, Quantization:quantization}"
)

# Supported model source types for an AI Manager model source.
MODEL_SOURCE_TYPES = ["HuggingFace"]

# Built-in roles assigned to the caller after a successful create/namespace add.
# 'Azure AIManager Contributor' is an ARM (control-plane) role scoped to the AI Manager
# resource; it is inherited by child namespaces, so it is only assigned at the AI Manager
# scope. 'Azure AIManager and namespace RBAC Reader' is a Kubernetes (data-plane) read
# role: at the AI Manager scope it grants read across all namespaces, and at a namespace
# scope it grants read to that single namespace.
AIMANAGER_CONTRIBUTOR_ROLE = "Azure AIManager Contributor"
AIMANAGER_NAMESPACE_READER_ROLE = "Azure AIManager and namespace RBAC Reader"

# Roles granted to the caller on 'az aimanager create' (AI Manager scope).
AIMANAGER_CALLER_ROLES = [AIMANAGER_CONTRIBUTOR_ROLE, AIMANAGER_NAMESPACE_READER_ROLE]

# Roles granted to the caller on 'az aimanager namespace add' (namespace scope). The
# Contributor role is intentionally omitted here because it is already inherited from the
# AI Manager scope, so only the data-plane Reader role is scoped to the new namespace.
NAMESPACE_CALLER_ROLES = [AIMANAGER_NAMESPACE_READER_ROLE]
