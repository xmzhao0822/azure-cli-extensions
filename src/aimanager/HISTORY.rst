.. :changelog:

Release History
===============

1.6.0
++++++
* ``az aimanager model show`` and ``az aimanager model calculate-cost``: Accept the human-readable
  model ID in ``<org>/<repo>`` form (e.g. ``microsoft/Phi-4-mini-instruct``) via ``--model-id`` /
  ``--name`` / ``-n``, in addition to the opaque resource name. The resource name is resolved
  client-side, so no extra service calls are needed in the common case.
* ``az aimanager model list -o table``: Show the ``ModelId`` column first so the human-readable
  model ID is the primary identifier.

1.5.0
++++++
* ``az aimanager create`` and ``az aimanager namespace add``: On success, grant the caller the
  built-in ``Azure AIManager Contributor`` and ``Azure AIManager and namespace RBAC Reader``
  roles on the new resource (best-effort; requires Owner or User Access Administrator). Skipped
  with ``--no-wait``.

1.4.1
++++++
* ``az aimanager modelsource`` and ``az aimanager namespace modeldeployment``: Accept
  ``--manager`` and ``-m`` as aliases of ``--aimanager-name``.

1.4.0
+++++++
* Mark ``az aimanager`` command groups as preview.

1.3.0
+++++++
* Add ``az aimanager model`` commands (``show``, ``list`` and ``calculate-cost``) to browse the
  regional AI model catalog and estimate the cost of deploying a model.
* Add ``az aimanager modelsource`` commands (``add``, ``update``, ``list``, ``show``,
  ``delete`` and ``wait``) to manage the model sources of an AI Manager.
* ``az aimanager namespace``: Add ``list-accesskeys`` and ``rotate-accesskeys`` commands to
  read and rotate the namespace LLM gateway API keys.
* ``az aimanager namespace``: Accept ``--aimanager-name`` as an alias of ``--manager``/``-m``
  for consistency with ``az aimanager namespace modeldeployment``.

1.2.0
++++++
* Add ``az aimanager namespace modeldeployment`` commands to add, update, list, show, delete,
  and wait for model deployments.

1.1.0
++++++
* ``az aimanager``: Add ``get-credentials`` command to retrieve the AI Manager kubeconfig.
* ``az aimanager namespace``: Add ``get-credentials`` command to retrieve the namespace kubeconfig.

1.0.0
++++++
* Initial release.
* ``az aimanager``: Add ``create``, ``update``, ``list``, ``show``, ``delete`` and
  ``namespace add/update/list/show/delete`` commands for AI Manager, backed by the vendored
  ``azure-mgmt-containerserviceaimanager`` SDK.
