from azureml.core.authentication import InteractiveLoginAuthentication
from azureml.core.compute import AmlCompute, ComputeTarget
from azureml.exceptions import ComputeTargetException
# azureml-core of version 1.0.72 or higher is required
from azureml.core import Workspace, Dataset
from azureml.data.datapath import DataPath



def setup_workspace():
    interactive_auth = InteractiveLoginAuthentication(tenant_id=TENANT_ID)

    ws = Workspace.create(
        auth=interactive_auth,
        storage_account='subscriptions/dc05bfc2-9d19-4ed0-8b82-f39054603103/resourcegroups/G4-PROJECT15/providers/microsoft.storage/storageaccounts/project15',
        name='abhishekh-project15',
        subscription_id='dc05bfc2-9d19-4ed0-8b82-f39054603103',
        resource_group='G4-PROJECT15',
        create_resource_group=False,
        location='eastus2',
        exist_ok=False
    )
    ws.write_config()

    print(Workspace.list('dc05bfc2-9d19-4ed0-8b82-f39054603103'))
    print('workspace setup')


def connect_to_workspace(config_file_name):
    interactive_auth = InteractiveLoginAuthentication(tenant_id=TENANT_ID)
    ws = Workspace.from_config(path=config_file_name, auth=interactive_auth)
    return ws


def connect_to_dataset_download():
    workspace = Workspace(subscription_id, resource_group, workspace_name)
    compute_target = ComputeTarget(workspace=workspace, name=COMPUTE_NAME)

    workspace = Workspace(subscription_id, resource_group, workspace_name)

    dataset = Dataset.get_by_name(workspace, name='elephant-segement-dataset')
    dataset.download('segments/test/')

    print('done')
