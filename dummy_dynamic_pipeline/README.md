# dummy_dynamic_pipeline
1. Register environment under environments folder:
   az ml component create --file dynamic-env.yaml
    Then using the registered environment in components/dynamic_subgraph/dynamic_subgraph.yaml

2. Register all the components to your workspace by using:
    az ml component create --file yaml_file

3. How to change to use your own compute cluster:
- Change the default_compute_target value in dynamic_pipeline.py

4. How to submit the pipeline to your own workspace:
- Change the fields in config.json to your own workspace.

5.  How to run the pipeline - cmd: python dynamic_pipeline.py

6. Notes:
- If use compute instance, then no any permission assign need to be done.
- If use compute cluster, then: there should be a managed identity assigned to the compute cluster. And:
-- that managed identity need to have the "Storage Blob Data Contributor" role to the blob storage account.
-- that managed identity need to have the "Contributor" role to the workspace.
