# dummy_dynamic_pipeline
1. Register all the components to your workspace.

2. How to change to use your own compute cluster:
- Change the default_compute_target value in dynamic_pipeline.py

3. How to submit the pipeline to your own workspace:
- Change the fields in config.json to your own workspace.

4. How to run the pipeline - cmd: python dynamic_pipeline.py

5. Notes:
- If use compute instance, then no any permission assign need to be done.
- If use compute cluster, then: there should be a managed identity assigned to the compute cluster. And:
-- that managed identity need to have the "Storage Blob Data Contributor" role to the blob storage account.
-- that managed identity need to have the "Contributor" role to the workspace.