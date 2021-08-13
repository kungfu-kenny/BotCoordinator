import os
from dotenv import load_dotenv

load_dotenv()

bot_key = os.getenv('BOT_KEY')
separator = '96ba108c-e5ea-4aeb-bd51-5da39b758192-9ba2af35-8981-41f4-980f-13bbf18fcdfb'
chat_id_default = os.getenv('CHAT_ID_DEFAULT')

folder_config = 'config'
name_db = 'projects.db'
name_loc_default = "Name Default"

table_users = 'users'
table_locations = 'locations'
table_groups = 'groups'
table_users_settings = 'users_settings'
table_users_locations = 'users_locations'
table_users_groups = 'users_groups'
table_groups_selected = 'groups_selected'

callback_sep_set = "⚙️"
callback_sep_sup = "💰" 
callback_sep_loc = "🌐"
callback_sep_gro = "🎻"

callback_sep_addloc = "111"
callback_sep_senloc = "112"
callback_sep_group_search = "221"
callback_sep_group_mine = "222"

callback_settings_update = '311'
callback_settings_groups = '321'
callback_settings_locations = '322'
callback_settings_default_name = '331'
callback_settings_default_text = '332'
callback_settings_default_minute = '333'

callback_sep_loc_show = 'w'
callback_sep_loc_del = 'z'
callback_sep_loc_next = "l"
callback_sep_group_upd = "u"
callback_sep_group_next = "x"
callback_sep_group_check = "c"

button_location_show = "Show 📍"
button_groups_mine_del = '❌'
button_groups_mine_check = 'Check ❔'
button_groups_mine_prev = '⬅️'
button_groups_mine_next = '➡️'
button_groups_mine_text = 'All added groups:'

button_settings_mine_text = 'My Settings:'
button_settings_message = 'My Message:'
button_settings_timing = 'My Timing:'
button_settings_name_default = 'Default Name:'

button_update = 'Update 🔄'
button_help = 'Help ❓'
button_settings = 'Settings ⚙️'
button_support = "Support 💰"
button_locations = 'Locations 🌐'
button_groups = 'Groups 🎻'
button_change = 'Change'

button_present = '✅'
button_absent = '❌'

button_location_add = "Add location"
button_location_send = "Resend location"

button_group_search = "Search Groups"
button_group_mine = 'My groups'

entrance_values = "Welcome to the Group Management"
entrance_bot_usage = "Niko, let\'s go bowling"
entrance_bot_img_name = 'roman.jpg'
entrance_bot_img_link = os.getenv('IMG_ROMAN')
entrance_bot_check_group = "This is a test message for check that bot is abandonded here"
entrance_bot_check_true = 'Group is fully functioning, everything is okay'
entrance_bot_check_false = "Unfortunatelly, this group is not working properly. We recommend you to remove group from the list"
entrance_update_good = "We successfully synchronized values of the groups hich you added to the bot"
entrance_update_bad = "Unfortunatelly, faced some problems with adding groups to database"
entrance_groups_list = 'Select what to do with groups:'
entrance_locations_absent = "You didn't provide any locations; please add them later"
entrance_groups_absent = "You didn't provide any groups; please add them later"

command_name_start = 'start'
command_name_location_add = 'add_location_name'
command_name_location_edit = 'edit_location_name'
command_name_group_update = 'edit_group_value'

value_limit = 10
value_limit_groups = 2
value_limit_locations = 5
value_message_default = 15
value_message_selection_default = 1
const = -0.4

callback_next_group = 'next_group_list'
callback_delete_group = 'update_group_list'
callback_next_loc = 'next_loc_list'
callback_delete_loc = 'update_loc_list'
callback_show_loc = 'show_loc_list'
callback_check_group = 'check_group_val'