# dummy_dynamic_pipeline
1. How to run the pipeline - cmd: python dynamic_pipeline.py
2. Notes:
- It needs to be executed in a compute cluster instead of compute instance, otherwise, you will encounter: Content: SSO failure: invalid request.
- There should be managed identity assigned to the compute cluster. And that managed identity need to have the "Storage Blob Data Contributor" role to the storage account.