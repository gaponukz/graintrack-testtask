from environs import Env

env = Env()
env.read_env()

with env.prefixed("APP_"):
    DB_CONFIG = env.json("DB_CONFIG")
