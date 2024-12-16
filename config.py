from os import environ
import re

id_pattern = re.compile(r'^.\d+$')

# bot
API_ID = int(environ.get('API_ID', '13963336'))
API_HASH = environ.get('API_HASH', 'a144d1e22ef0b29738e8c00713d02678')
BOT_TOKEN = environ.get('BOT_TOKEN', '6839308980:AAGPMRBu1WTb7YLwjk1fVXofsP9S0QgYvoQ')
ADMINS = [int(admins) if id_pattern.search(admins) else admins for admins in environ.get('ADMINS', '7427294551').split()]

# bs
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', '-1002285787659'))
fsub_eid = environ.get('FSUB_ID')
FSUB_ID = int(fsub_eid) if fsub_eid and id_pattern.search(fsub_eid) else None

# database

DATABASE_URL = environ.get('DATABASE_URL', 'mongodb+srv://chatgpt:chatgpt123@caption.27mvj.mongodb.net/?retryWrites=true&w=majority&appName=Caption')
