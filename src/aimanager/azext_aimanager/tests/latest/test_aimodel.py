# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock

from azure.cli.core.azclierror import InvalidArgumentValueError
from azure.core.exceptions import ResourceNotFoundError

from azext_aimanager import custom
from azext_aimanager._validators import validate_ai_model_name
from azext_aimanager.vendored_sdks.v2026_05_02_preview import models


class MockCmd:
    def get_models(self, name, **_):
        return getattr(models, name)


class TestAIModel(unittest.TestCase):

    def setUp(self):
        self.cmd = MockCmd()
        self.client = MagicMock()

    def test_show_aimodel(self):
        self.client.get.return_value = "model"

        result = custom.show_aimodel(self.cmd, self.client, "eastus2", "9806f0c862fdd920")

        self.assertEqual(result, "model")
        self.client.get.assert_called_once_with("eastus2", "9806f0c862fdd920")

    def test_show_aimodel_by_model_id_derives_resource_name(self):
        self.client.get.return_value = "model"

        result = custom.show_aimodel(
            self.cmd, self.client, "eastus2", "microsoft/Phi-4-mini-instruct")

        self.assertEqual(result, "model")
        # SHA-256('microsoft/Phi-4-mini-instruct')[:8].hex() == '9806f0c862fdd920'
        self.client.get.assert_called_once_with("eastus2", "9806f0c862fdd920")
        self.client.list.assert_not_called()

    def test_show_aimodel_by_model_id_falls_back_to_catalog_scan(self):
        # A mismatched-casing model ID does not hash to the canonical name, so the
        # first get raises NotFound and the command scans the catalog.
        self.client.get.side_effect = [ResourceNotFoundError("nope"), "model"]
        self.client.list.return_value = [
            SimpleNamespace(
                name="9806f0c862fdd920",
                properties=SimpleNamespace(model_id="microsoft/Phi-4-mini-instruct")),
        ]

        result = custom.show_aimodel(
            self.cmd, self.client, "eastus2", "microsoft/phi-4-MINI-instruct")

        self.assertEqual(result, "model")
        self.assertEqual(self.client.get.call_count, 2)
        self.client.get.assert_called_with("eastus2", "9806f0c862fdd920")

    def test_show_aimodel_by_unknown_model_id_raises_not_found(self):
        self.client.get.side_effect = ResourceNotFoundError("nope")
        self.client.list.return_value = []

        with self.assertRaises(ResourceNotFoundError):
            custom.show_aimodel(self.cmd, self.client, "eastus2", "unknown/model")

    def test_list_aimodel(self):
        self.client.list.return_value = ["model"]

        result = custom.list_aimodel(self.cmd, self.client, "eastus2")

        self.assertEqual(result, ["model"])
        self.client.list.assert_called_once_with("eastus2")

    def test_calculate_aimodel_cost_sends_empty_request_body(self):
        self.client.calculate_cost.return_value = "plans"

        result = custom.calculate_aimodel_cost(
            self.cmd, self.client, "eastus2", "9806f0c862fdd920")

        self.assertEqual(result, "plans")
        self.client.calculate_cost.assert_called_once()
        location, ai_model_name, body = self.client.calculate_cost.call_args[0]
        self.assertEqual(location, "eastus2")
        self.assertEqual(ai_model_name, "9806f0c862fdd920")
        self.assertIsInstance(body, models.CalculateCostRequest)
        self.assertEqual(dict(body), {})

    def test_calculate_aimodel_cost_by_model_id_derives_resource_name(self):
        self.client.calculate_cost.return_value = "plans"

        result = custom.calculate_aimodel_cost(
            self.cmd, self.client, "eastus2", "microsoft/Phi-4-mini-instruct")

        self.assertEqual(result, "plans")
        location, ai_model_name, _ = self.client.calculate_cost.call_args[0]
        self.assertEqual(location, "eastus2")
        self.assertEqual(ai_model_name, "9806f0c862fdd920")


class TestAIModelValidators(unittest.TestCase):

    def test_valid_name(self):
        validate_ai_model_name(SimpleNamespace(ai_model_name="9806f0c862fdd920"))

    def test_missing_name_is_allowed(self):
        validate_ai_model_name(SimpleNamespace(ai_model_name=None))
        validate_ai_model_name(SimpleNamespace())

    def test_blank_name_is_rejected(self):
        with self.assertRaises(InvalidArgumentValueError):
            validate_ai_model_name(SimpleNamespace(ai_model_name="   "))


if __name__ == '__main__':
    unittest.main()
