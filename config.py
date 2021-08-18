from environs import Env


env = Env()
env.read_env()

secret_key = env.str('SECRET_KEY', 'REPLACE_ME')
