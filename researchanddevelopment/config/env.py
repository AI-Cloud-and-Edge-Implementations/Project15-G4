from environs import Env

env = Env()
env.read_env()

DEVICE_CONNECTION_STRING = env("DEVICE_CONNECTION_STRING")