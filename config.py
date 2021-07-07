import os
from dotenv import load_dotenv

load_dotenv()

bot_key = os.getenv('BOT_KEY')
chat_id_default = os.getenv('CHAT_ID_DEFAULT')

folder_config = 'config'
name_db = 'projects.db'

table_users = 'users'
table_locations = 'locations'
table_groups = 'groups'
table_users_locations = 'users_locations'
table_users_groups = 'users_groups'