from environs import Env
from elephantcallscounter.common import constants

environment_loader = Env()
environment_loader.read_env()

DEVICE_CONNECTION_STRING = environment_loader("DEVICE_CONNECTION_STRING", default='')
STORAGE_SAS_KEY = environment_loader("STORAGE_ACCOUNT_SAS_KEY")
CONNECTION_STRING = environment_loader("CONNECTION_STRING")
AZURE_STORAGE_ACCOUNT = environment_loader("AZURE_STORAGE_ACCOUNT")
TRAINING_FILE_PATH = environment_loader(
    "TRAINING_FILE_PATH",
    default=constants.TRAINING_FILE_PATH_DEFAULT
)
TEST_FILE_PATH = environment_loader(
    "TEST_FILE_PATH",
    default=constants.TEST_PATH_DEFAULT
)
IOT_HUB_CONN_STRING = environment_loader("IOT_HUB_CONN_STRING")
