from environs import Env


env = Env()
env.read_env()

secret_key = env.str('SECRET_KEY', 'REPLACE_ME')
secret_token_key = env.str('SECRET_TOKEN_KEY', 'REPLACE_ME')
database = env.str('DATABASE', 'fastApi')
db_user = env.str('DB_USER')
db_password = env.str('DB_PASSWORD')
db_host = env.str('DB_HOST')
db_port = env.str('DB_PORT')
