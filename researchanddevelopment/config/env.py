from environs import Env

environment_loader = Env()
environment_loader.read_env()

DEVICE_CONNECTION_STRING = environment_loader("DEVICE_CONNECTION_STRING", default='')
STORAGE_SAS_KEY = environment_loader("STORAGE_ACCOUNT_SAS_KEY")
