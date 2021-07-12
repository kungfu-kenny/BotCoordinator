import os
from dotenv import load_dotenv

load_dotenv()

bot_key = os.getenv('BOT_KEY')
separator = '96ba108c-e5ea-4aeb-bd51-5da39b758192-9ba2af35-8981-41f4-980f-13bbf18fcdfb'
chat_id_default = os.getenv('CHAT_ID_DEFAULT')

folder_config = 'config'
name_db = 'projects.db'

table_users = 'users'
table_locations = 'locations'
table_groups = 'groups'
table_users_locations = 'users_locations'
table_users_groups = 'users_groups'

button_update = 'Update'
button_help = 'Help'
button_settings = 'Settings'
button_support = "Support"
button_locations = 'Locations'
button_groups = 'Groups'

button_location_add = "Add location"
button_location_send = "Resend location"

entrance_values = "Welcome to the Group Management"
entrance_bot_usage = "Nico, let's go bowling"
entrance_bot_img_name = 'roman.jpg'
entrance_bot_img_link = os.getenv('IMG_ROMAN')