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

# Built-in roles assigned to the caller when an AI Manager or namespace is created.
# 'Azure AIManager Contributor' is an ARM (control-plane) RBAC role, while
# 'Azure AIManager and namespace RBAC Reader' is a Kubernetes (data-plane) RBAC role.
AIMANAGER_CONTRIBUTOR_ROLE = "Azure AIManager Contributor"
AIMANAGER_NAMESPACE_READER_ROLE = "Azure AIManager and namespace RBAC Reader"
DEFAULT_CALLER_ROLES = [AIMANAGER_CONTRIBUTOR_ROLE, AIMANAGER_NAMESPACE_READER_ROLE]
