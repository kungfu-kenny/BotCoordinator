import os
import sqlite3
from sqlite3.dbapi2 import Connection
from telegram_manager import TelegramManager
from config import (name_db,
                    value_limit,
                    folder_config,
                    entrance_bot_usage,
                    name_loc_default,
                    name_join_default,
                    value_old_default,
                    value_limit_search,
                    value_message_default,
                    value_message_selection_default,
                    table_poll,
                    table_users,
                    table_groups,
                    table_locations,
                    table_poll_groups,
                    table_users_groups,
                    table_users_settings,
                    table_groups_selected,
                    table_users_locations,
                    table_user_group_connect)


class DataUsage:
    """
    class which is dedicated to produce the values of the 
    """
    def __init__(self) -> None:
        self.folder_current = os.getcwd()
        self.telegram_manager = TelegramManager()
        self.folder_config = os.path.join(self.folder_current, folder_config)
        self.create_folder = lambda x: os.path.exists(x) or os.mkdir(x)
        self.produce_values()

    def proceed_error(self, msg:str) -> None:
        """
        Method which is dedicated to send errors
        Input:  msg = message of the error
        Output: we printed and send to the telegram
        """
        print(msg)
        self.telegram_manager.proceed_message_values(msg)
            
    def check_db(self) -> None:
        """
        Test method for checking the database values
        """
        a = self.cursor.execute(f'SELECT * from {table_users};').fetchall()
        print(a)
        print('#################################################')
        b = self.cursor.execute(f'SELECT * from {table_groups};').fetchall()
        print(b)
        print('#################################################')
        c = self.cursor.execute(f'SELECT * from {table_users_groups};').fetchall()
        print(c)
        print('#################################################')
        d = self.cursor.execute(f"SELECT * FROM {table_users_settings};").fetchall()
        print(d)
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        e = self.get_search_button_basic()
        print(e)
        print('________________________________________________________')

    def create_connection(self) -> None:
        """
        Method which is dedicated to produce the connection of the 
        Input:  None
        Output: we created the database
        """
        try:
            self.create_folder(self.folder_config)
            self.connection = sqlite3.connect(self.name_db, check_same_thread=False)
            self.cursor = self.connection.cursor()
        except Exception as e:
            msg = f'We faced problems with the connection. Reason: {e}'
            self.proceed_error(msg)

    def close_connection(self) -> None:
        """
        Method which is dedicated to close the 
        Input:  None
        Output: we closed the connection to the database
        """
        self.connection.close()

    def return_user_values(self, id_user:int) -> set:
        """
        Method which is dedicated to return
        Input:  id_user = id of the selected user
        Output: list with values
        """
        try:
            value_return = self.cursor.execute(f"SELECT name_first, name_last, nickname FROM {table_users} WHERE id={id_user};").fetchone()
            return value_return
        except Exception as e:
            msg = f"We faced problems with the getting of the user; Mistake: {e}"
            self.proceed_error(msg)
            return []

    def update_user_information(self, value_list:list) -> None:
        """
        Method which is dedicated to produce the changes of the user values
        Input:  value_list = list value of the format [name_first, name_last, username, user_id]
        Output: we successfully updated all these values
        """
        try:
            self.cursor.execute(f"UPDATE {table_users} SET name_first=?, name_last=?, nickname=? WHERE id=?;", value_list)
            self.connection.commit()
        except Exception as e:
            msg = f"We faced problems with updating all name values; Mistake: {e}"
            self.proceed_error(msg)

    def update_text_message(self, id_user:int, text_new:str) -> bool:
        """
        Method which is dedicated to update sent text
        Input:  id_user = id of the selected user
                text_new = text which is dedicated to get updated
        Output: boolean value which signifies that you updated value succesfully
        """
        try:
            self.cursor.execute(f"UPDATE {table_users_settings} SET text_sending = ? WHERE id_user = ?;", (text_new, id_user))
            self.connection.commit()
            return True
        except Exception as e:
            msg = f"We face problems with updating the message text; Mistake: {e}"
            self.proceed_error(msg)
            return False

    def update_name_default(self, id_user:int, text_new:str) -> bool:
        """
        Method which is dedicated to update sent text
        Input:  id_user = id of the selected user
                text_new = text which is dedicated to get updated
        Output: boolean value which signifies that you updated value succesfully
        """
        try:
            self.cursor.execute(f"UPDATE {table_users_settings} SET name_default = ? WHERE id_user = ?;", (text_new, id_user))
            self.connection.commit()
            return True
        except Exception as e:
            msg = f"We face problems with updating the default name; Mistake: {e}"
            self.proceed_error(msg)
            return False

    def update_time_default(self, id_user:int, time_new:int) -> bool:
        """
        Method which is dedicated to update sent text
        Input:  id_user = id of the selected user
                text_new = text which is dedicated to get updated
        Output: boolean value which signifies that you updated value succesfully
        """
        try:
            self.cursor.execute(f"UPDATE {table_users_settings} SET text_minutes = ? WHERE id_user = ?;", (time_new, id_user))
            self.connection.commit()
            return True
        except Exception as e:
            msg = f"We face problems with updating the default name; Mistake: {e}"
            self.proceed_error(msg)
            return False

    def check_presence_locations(self, id_user:int) -> bool:
        """
        Method which is dedicated to check presence of the locations in the
        Input:  id_user = id to check values
        Output: booelan which signifies presence location for user
        """
        try:
            value_list = self.cursor.execute(f"SELECT * FROM {table_users_locations} where id_user={id_user};").fetchone()
            if value_list:
                return True
            return False
        except Exception as e:
            msg = f"We faced problems with checking the locations. Error: {e}"
            self.proceed_error(msg)
            return False

    def check_presence_groups(self, id_user:int) -> bool:
        """
        Method which is dedicated to check presence of selected group by user
        Input:  id_user = id to check values
        Output: boolean value which signifies presence groups for user
        """
        try:
            value_list = self.cursor.execute(f"SELECT * FROM {table_users_groups} where id_user={id_user};").fetchone()
            if value_list:
                return True
            return False
        except Exception as e:
            msg = f"We faced problems with checking the groups for users. Error: {e}"
            self.proceed_error(msg)
            return False

    def get_user_values(self, id_user:int) -> bool:
        """
        Method which is dedicated to check the presence of the 
        Input:  id_user = user id which is checked to this mission
        Output: we successfully checked presence the use within the bot
        """
        try:
            value_user = self.cursor.execute(f'SELECT id from {table_users} where id={id_user}').fetchone()
            if value_user:
                return True
            return False
        except Exception as e:
            msg = f'We found problems with checking values of the previous insertion, mistake: {e}'
            self.proceed_error(msg)

    def get_user_groups(self, id_chat:int, id_limit:int=0) -> set:
        """
        Method which is dedicated to return values of the groups and group names
        Input:  id_chat = id of the chat which was using this feature
        Output: set with lists of the values with the groups and names
        """
        try:
            if id_limit:
                value_groups = self.cursor.execute(f"SELECT id_group FROM {table_users_groups} WHERE id_user={id_chat} LIMIT {id_limit};").fetchall()
            else:
                value_groups = self.cursor.execute(f"SELECT id_group FROM {table_users_groups} WHERE id_user={id_chat};").fetchall()
            value_groups = []
            return value_groups
        except Exception as e:
            msg = f"We found problems with returning groups to values, mistake: {e}"
            self.proceed_error(msg)
            return []

    def remove_location_manually(self, value_list:list) -> bool:
        """
        Method which is dedicated to remove values of the
        Input:  value_list = id of the user, latitude and longitude of the user
        Output: set with boolean that everything is okay and names of the coordinates which were removed
        """
        value_return = []
        try:
            value_id, value_latitude, value_longitude = value_list
            values_id = self.cursor.execute(f"SELECT id_location FROM {table_users_locations} WHERE id_user={value_id};").fetchall()
            values_id = [str(v[0]) for v in values_id]
            values_id_str = ','.join(values_id)
            if values_id_str:
                value_names = self.cursor.execute(
                    f"SELECT name_location FROM {table_locations} WHERE id IN ({values_id_str}) AND latitude={value_latitude} AND longitude={value_longitude};"
                    ).fetchall()
                if value_names:
                    value_return = [f[0] for f in value_names]
                self.cursor.execute(f"DELETE FROM {table_users_locations} WHERE id_user={value_id} AND id_location IN ({values_id_str});")
                self.cursor.execute(
                    f"DELETE FROM {table_locations} WHERE id IN ({values_id_str}) AND latitude={value_latitude} AND longitude={value_longitude};").fetchall()
                self.connection.commit()
            return True, value_return
        except Exception as e:
            msg = f"We faced problems with the deletion of the location in that cases; Mistake: {e}"
            self.proceed_error(msg)
            return False, value_return

    def get_user_coordinate(self, id_chat:int, id_location:int) -> list:
        """
        Method which is dedicated to get location for the user 
        Input:  id_chat = chat which required coordinates
                id_location = id of the location of selected user
        Output: we returned list values from the 
        """
        try:
            #TODO add check on the checking the coordinates
            value_list = self.cursor.execute(f"SELECT * FROM {table_locations} WHERE id={id_location};").fetchone()
            if value_list:
                return value_list
            return []
        except Exception as e:
            msg = f"We found problems with returning elected coordinate to the selected user, mistake: {e}"
            self.proceed_error(msg)
            return []

    def delete_location_user(self, id_chat:int, id_location:int) -> None:
        """
        Method which is dedicated to delete location from the
        Input:  id_chat = chat id value
                id_location = id of the location for the user
        Output: We successfully deleted values of the location
        """
        try:
            self.cursor.execute(f"DELETE FROM {table_users_locations} WHERE id_user={id_chat} AND id_location={id_location};")
            self.cursor.execute(f"DELETE FROM {table_locations} WHERE id={id_location};")
            self.connection.commit()
        except Exception as e:
            msg = f'We faced problems with the deleting locations from the database. Mistake: {e}'
            self.proceed_error(msg)

    def get_group_values(self, group_id:int, group_name:str) -> bool:
        """
        Method which is dedicated to check the presence of selected group or update name in other cases
        Input:  group_id = id of selected group
                group_name = name of the selected group
        Output: boolean value which shows presence of the 
        """
        try:
            value_list = self.cursor.execute(f"SELECT id, name FROM {table_groups} WHERE id={group_id};").fetchone()
            if not value_list:
                return False
            group_used_id, group_used_name = value_list
            if group_used_name != group_name:
                self.cursor.execute(f"UPDATE {table_groups} SET name={group_name} WHERE id={group_used_id};")
                self.connection.commit()
            return True
        except Exception as e:
            msg = f"We faced problems with checking of the group prensence. Mistake: {e}"
            self.proceed_error(msg)
            return False

    def get_search_button_basic(self, groups_limit:int=value_limit_search) -> list:
        """
        Method which is dedicated to make basic search 
        Input:  groups_limit = limitations to the returnal of groups
        Output: we get search values of the lists
        """
        try:
            value_list = self.cursor.execute(f"SELECT id, name FROM {table_groups} ORDER BY date_value DESC LIMIT({groups_limit});").fetchall()
            return value_list
        except Exception as e:
            msg = f"We faced problems with get basic search groups. Mistake: {e}"
            self.proceed_error(msg)
            return []

    def get_search_button_manually(self, input_string:str, groups_limit:int=value_limit_search) -> list:
        """
        Method which is dedicated to make manual search of the groups for the more clear usage of it
        Input:  input_string = input string from the user
                groups_limit = limitations for the returnal of groups
        Output: we get groups for user to manually search
        """
        try:
            value_list = self.cursor.execute(
                f"SELECT id, name FROM {table_groups} WHERE name LIKE %?% ORDER BY date_value DESC LIMIT({groups_limit});", (input_string,)).fetchall()         
            return value_list
        except Exception as e:
            msg = f"We faced problems with getting manual search groups. Mistake: {e}"
            self.proceed_error(msg)
            return []

    def produce_insert_group_user_connect(self, id_user:int, id_group:int, connect_name:str=name_join_default) -> bool:
        """
        Method which is dedicated to make 
        Input:  id_user = id of the user which must b used
                id_group = id of the group which is required to make
                connect_name = connected names with the values
        Output: inserted values to the table which i required to make the connection
        """
        try:
            self.cursor.execute(f"INSERT INTO {table_user_group_connect}(id_user, id_group, text_message) VALUES (?,?,?);", 
                                (id_user, id_group, connect_name))
            self.connection.commit()
            return True
        except Exception as e:
            msg = f"We faced problems with the setting the connection table of user and group. Mistake: {e}"
            self.proceed_error(msg)
            return False

    def check_insert_group_user(self, id_user:int, id_group:int) -> bool:
        """
        Method which is dedicated to check inserted this values previously
        Input:  id_user = id of the user
                id_group = id of the group
        Output: boolean value which signifies that we already made this
        """
        try:
            value_list = self.cursor.execute(f"SELECT * FROM {table_user_group_connect} WHERE id_user={id_user} AND id_group={id_group};").fetchone()
            if value_list:
                return True
            return False
        except Exception as e:
            msg = f"We faced problems with the check previous insertion on th. Mistake: {e} "
            self.proceed_error(msg)
            return False

    def return_inserted_message(self, id_user:int, id_group:int) -> str:
        """
        Method which is dedicated to return previously 
        Input:  id_user = id of the user
                id_group = id of the group
        Output: string value which user is required to send
        """
        try:
            value_string = self.cursor.execute(f"SELECT text_message FROM {table_user_group_connect} WHERE id_user={id_user} AND id_group={id_group};").fetchone()
            if value_string:
                return value_string[0]
            return ''
        except Exception as e:
            msg = f"We found problems with getting message of groups to resend; Mistake: {e}"
            self.proceed_error(msg)
            return ''

    def delete_user_group_values(self, id_user:int, id_group:int) -> None:
        """
        Method which is dedicated to remove this value in cases of we connected groups
        Input:  id_user = id of the user
                id_group = id of this group
        Output: We removed all possibl values
        """
        try:
            self.cursor.execute(f"DELETE FROM {table_user_group_connect} WHERE id_user={id_user} AND id_group={id_group};")
            self.connection.commit()
        except Exception as e:
            msg = f"We faced problems ith deletion from {table_user_group_connect} table, Mistake: {e}"
            self.proceed_error(msg)

    def return_group_values(self, id_user:int) -> set:
        """
        Method which is dedicated to return for the user group values
        Input:  id_user = id of the selected user
        Output: list of lists with the 
        """
        try:
            value_list_id = self.cursor.execute(f"SELECT id_group FROM {table_users_groups} WHERE id_user={id_user};").fetchall()
            if not value_list_id:
                return [], []
            value_list_id = ','.join([str(v[0]) for v in value_list_id])
            value_list_group = self.cursor.execute(f"SELECT id, name FROM {table_groups} WHERE id IN ({value_list_id});").fetchall()
            return [v[0] for v in value_list_group], [v[1] for v in value_list_group]
        except Exception as e:
            msg = f"We faced problems with getting values of the groups to the user; Mistake: {e}"
            self.proceed_error(msg)
            return [], []

    def get_current_id(self) -> int:
        """
        Method which is dedicated to manually return values from the database manually
        Input:  None
        Output: we successfully returned last id of the coordinate
        """
        try:
            return self.cursor.execute(f"SELECT MAX(id) FROM {table_locations};").fetchone()
        except Exception as e:
            msg = f'We faced some problems with the getting last id value. Mistake: {e}'
            self.proceed_error(msg)
            return -1

    def insert_location(self, id_list:list, name_location:str, latitude:float, longitude:float) -> bool:
        """
        Method which is dedicated to insert location to the values
        Input:  id_list = list of the user values which inserted location
                name_location = name of the location which we would add
                latitude = latitude of the coordinates
                longitude = longitude of the coordinates
        Output: we successfully inserted coordinates and 
        """
        try:
            id_user, username, name_first, name_last = id_list
            self.insert_settings(id_user)
            if not self.get_user_values(id_user):
                self.insert_username(id_user, username, name_first, name_last)
            self.cursor.execute(f"INSERT INTO {table_locations} (name_location, latitude, longitude) VALUES (?, ?, ?);", 
                                (name_location, latitude, longitude))
            self.cursor.execute(f"INSERT INTO {table_users_locations} (id_user, id_location) VALUES (?, ?);", (id_user, self.cursor.lastrowid))
            self.connection.commit()
            return True
        except Exception as e:
            msg = f'We faced problems with the performing of the operating of the location inserting. Mistake: {e}'
            self.proceed_error(msg)
            return False

    def make_group_insertion(self, group_id:int, group_name:str) -> bool:
        """
        Method which is dedicated to make the group insertion
        Input:  group_id = id of the selected values
                group_name = name of the group
        Output: we successfully created 
        """
        try:
            self.cursor.execute(f"INSERT INTO {table_groups} (id, name) VALUES (?, ?);", (group_id, group_name))
            self.connection.commit()
            return True
        except Exception as e:
            msg = f"We faced problems with isertion of the groups. Mistake: {e}"
            self.proceed_error(msg)
            return False

    def check_chat_id(self, id_chat:int) -> set:
        """
        Method which is dedicated to check that 
        Input:  id_chat = value chat which was previously used
        Output: boolean values for the check
        """
        try:        
            value_user = bool(self.cursor.execute(f"SELECT id FROM {table_users} WHERE id={id_chat};").fetchone())
            value_group = bool(self.cursor.execute(f"SELECT id FROM {table_groups} WHERE id={id_chat};").fetchone())
            return value_user, value_group
        except Exception as e:
            msg = f"We faced problems with check on which chat it can be used. Mistake: {e}"
            self.proceed_error(msg)
            return False, False

    def connect_user_group(self, id_group:int, id_user:int) -> bool:
        """
        Method which is dedicated to connect uer to the group
        Input:  id_group = id of selected user
                id_user = id of the telegram user
        Output: we inserted to the foreign keys values
        """
        try:
            self.cursor.execute(f"INSERT INTO {table_users_groups} (id_user, id_group) VALUES (?, ?);", (id_user, id_group))
            self.connection.commit()
            return True
        except Exception as e:
            msg = f'We have problems with the connection between user and group. Mistake: {e}'
            self.proceed_error(msg)
            return False

    def disconnect_whole_group(self, id_group:int) -> bool:
        """
        Method which is dedicated to remove whole group from the 
        Input:  id_group = id in the groups table
        Output: bool which signifies that we successfully removed all values
        """
        try:
            self.cursor.execute(f"DELETE FROM {table_groups} WHERE id={id_group};")
            self.connection.commit()
            return True
        except Exception as e:
            msg = f"We found problems with deletion of the whole group from the {table_groups} in database. Mistake: {e}"
            self.proceed_error(msg)
            return False

    def disconnect_user_group(self, id_user:int, id_group:int) -> set:
        """
        Method which is dedicated to remove connections between user and group
        Input:  id_user = value of the user id
                id_group = value of the group id
        Output: boolean value which signifies that we need to make further check and bool that all is okay
        """
        try:
            check_value = self.cursor.execute(f"SELECT COUNT(id_user) FROM {table_users_groups} WHERE id_group={id_group};").fetchone()
            check_value = check_value[0] if check_value else 0
            if check_value:
                self.cursor.execute(f"DELETE FROM {table_users_groups} WHERE id_user={id_user} AND id_group={id_group};")
                self.connection.commit() 
                if check_value == 1:
                    return True, True, True
                return True, False, True
            else:
                return True, False, False
        except Exception as e:
            msg = f'We have problems with the connection deletion between user and group. Mistake: {e}'
            self.proceed_error(msg)
            return False, False, False

    def check_user_group_connection(self, id_group:int, id_user:int) -> bool:
        """
        Method which is dedicated to check that user has added group to the connection
        Input:  id_group = id of the selected group
                id_user = id of the selected user
        Output: boolean value that signifies that we have successfully 
        """
        try:
            value_list = self.cursor.execute(f"SELECT * FROM {table_users_groups} WHERE id_group={id_group} AND id_user={id_user};").fetchone()
            if value_list:
                return True
            return False
        except Exception as e:
            msg = f"We have problem with getting values from the {table_users_groups}. Mistake: {e}"
            self.proceed_error(msg)
            return False

    def insert_group_additional(self, group_id:int, group_name:str) -> None:
        """
        Method which is dedicated to add groups
        Input:  group_id = id of the group
                group_name = name of the group
        Output: We added new group in that cases
        """
        try:
            if not self.get_group_values(group_id, group_name):
                self.make_group_insertion(group_id, group_name)
        except Exception as e:
            msg = f"We faced the problem with additional insertion of the values; Mistake: {e}"
            self.proceed_error(msg)

    def insert_user_group_additional(self, id_group:int, id_user:int) -> None:
        """
        Method which is dedicated to directly insert user_group
        Input:  id_group = id of the selected group
                id_user = id of the selected user
        Output: we created connection between user and group; None
        """
        try:
            if not self.check_user_group_connection(id_group, id_user):
                self.connect_user_group(id_group, id_user)
        except Exception as e:
            msg = f"We faced problems with additional insertion values; Mistake: {e}"
            self.proceed_error(msg)

    def insert_group(self, group_id:int, group_name:str, id_user:int, username:str, name_first:str, name_last:str) -> bool:
        """
        Method which is dedicated to insert group which was inserted to the 
        Input:  group_id = id of the group which was inserted
                group_name = name of the group
                id_user = user id values
                username = username of the telegram
                name_first = first name of the telegram user
                name_last = last name of the telegram user
        Output: we successfully inserted values of the group
        """
        try:
            self.insert_settings(id_user)
            if not self.get_user_values(id_user):
                self.insert_username(id_user, username, name_first, name_last)
            self.insert_group_additional(group_id, group_name)
            self.insert_user_group_additional(group_id, id_user)
            self.connection.commit()
            return True
        except Exception as e:
            msg = f"We faced problem with inserting the group. Mistake: {e}"
            self.proceed_error(msg)
            return False
            
    def insert_username(self, id_user:int, username:str, name_first:str, name_last:str) -> bool:
        """
        Method which is dedicated to insert username to the 
        Input:  id_username = id of the selected user
                name_first = first name of the user
                name_last = last name of the user
                username = username of the 
        Output: we inserted username values
        """
        try:
            self.cursor.execute(f"INSERT INTO {table_users}(id, name_first, name_last, nickname) VALUES (?, ?, ?, ?);", 
                        (id_user, name_first, name_last, username))
            self.connection.commit()
            return True
        except Exception as e:
            msg = f'We faced problem with inserting values within the database. Mistake: {e}'
            self.proceed_error(msg)
            return False

    def return_user_name_default_bool(self, id_user:int) -> bool:
        """
        Method to return values for the 
        Input:  id_user = user id from the telegram
        Output: boolean value for this values
        """
        try:
            name_default_boolean = self.cursor.execute(f"SELECT name_default_boolean FROM {table_users_settings} WHERE id_user={id_user};").fetchone()
            if not name_default_boolean:
                self.insert_settings(id_user)
                return self.return_user_name_default_bool(id_user)
            return bool(name_default_boolean[0])
        except Exception as e:
            msg = f"We faced problems with the work of the setting to the users. Mistake: {e}"
            self.proceed_error(msg)
            return False

    def update_user_settings_default_name(self, id_user:int) -> None:
        """
        Method which is dedicated to change the possibility of the default name
        Input:  id_user = id of all possible users between there
        Output: Non, but the boolean value was successfully inserted
        """
        try:
            value_selected = self.return_user_name_default_bool(id_user)
            value_bool_new = True if not value_selected else False
            self.cursor.execute(f"UPDATE {table_users_settings} SET name_default_boolean={value_bool_new} WHERE id_user={id_user};")
            self.connection.commit()
        except Exception as e:
            msg = f"We faced problems with the changing of the default name usage. Mistake: {e}"
            self.proceed_error(msg)

    def return_user_name_settings(self, id_user:int) -> str:
        """
        Method which is dedicated to return default location name
        Input:  id_user = user id
        Output: string of the default name
        """
        try:
            name_default = self.cursor.execute(f"SELECT name_default FROM {table_users_settings} WHERE id_user={id_user};").fetchone()
            if not name_default:
                self.insert_settings(id_user)
                return self.return_user_name_settings(id_user)
            return name_default[0]
        except Exception as e:
            msg = f"We faced problems with return default name. Mistake: {e}"
            self.proceed_error(msg)
            return name_loc_default

    def return_user_text(self, id_user:int) -> str:
        """
        Method which is dedicated to return default location name
        Input:  id_user = user id
        Output: string of the default name
        """
        try:
            name_default = self.cursor.execute(f"SELECT text_sending FROM {table_users_settings} WHERE id_user={id_user};").fetchone()
            if not name_default:
                self.insert_settings(id_user)
                return self.return_user_text(id_user)
            return name_default[0]
        except Exception as e:
            msg = f"We faced problems with return default text. Mistake: {e}"
            self.proceed_error(msg)
            return entrance_bot_usage

    def return_user_minutes(self, id_user:int) -> str:
        """
        Method which is dedicated to return default location name
        Input:  id_user = user id
        Output: string of the default name
        """
        try:
            name_default = self.cursor.execute(f"SELECT text_minutes FROM {table_users_settings} WHERE id_user={id_user};").fetchone()
            if not name_default:
                self.insert_settings(id_user)
                return self.return_user_minutes(id_user)
            return name_default[0]
        except Exception as e:
            msg = f"We faced problems with return default text. Mistake: {e}"
            self.proceed_error(msg)
            return value_message_default

    def return_user_settings(self, id_user:int) -> list:
        """
        Method which is dedicated to 
        Input:  id_user = id from the telebot
        Output: list with all values of the user's settings
        """
        try:
            value_settings = self.cursor.execute(f"SELECT * FROM {table_users_settings} WHERE id_user={id_user};").fetchone()
            if not value_settings:
                self.insert_settings(id_user)
                return self.return_user_settings(id_user)
            return value_settings
        except Exception as e:
            msg = f"We faced problems with the work of the setting to the users. Mistake: {e}"
            self.proceed_error(msg)
            return []

    def insert_settings(self, id_user:int) -> bool:
        """
        Method which is dedicated to insert the values to the 
        Input:  id_user = user id value which requires for that
        Output: boolean value which signifies that everything 
        """
        try:
            value_check = self.cursor.execute(f"SELECT id_user FROM {table_users_settings} WHERE id_user={id_user};").fetchone()
            if not value_check:
                self.cursor.execute(f"INSERT INTO {table_users_settings}(id_user) VALUES ({id_user});")
                self.connection.commit()
            return True
        except Exception as e:
            msg = f'We faced problem with inserted settings to the user. Mistake: {e}'
            self.proceed_error(msg)
            return False

    def get_user_coordinates(self, id:int) -> set:
        """
        Method which is dedicated to produce the user coordinates of the 
        Input:  id = id of the user which is required to find them
        Output: list with the strings of coordinate names of the user, boolean with signifies maximum capacity
        """
        try:
            list_id = self.cursor.execute(f"SELECT id_location FROM {table_users_locations} WHERE id_user={id};").fetchall()
            if not list_id:
                return [], [], True
            list_id = [str(l[0]) for l in list_id]
            value_str = ','.join(list_id)
            value_list = self.cursor.execute(f"SELECT name_location from {table_locations} WHERE id IN ({value_str});").fetchall()
            return [f[0] for f in value_list], list_id, len(value_list) < value_limit
        except Exception as e:
            msg = f"We have problems with getting coordinates for the users. Mistake: {e}"
            self.proceed_error(msg)
            return [], [], False

    def get_length_settings(self, id_user:int) -> set:
        """
        Method which is dedicated to return values 
        Input:  id_user = id of the user
        Output: we returned values of length of the values
        """
        try:
            value_id_loc = self.cursor.execute(f"SELECT COUNT(*) FROM {table_users_locations} WHERE id_user={id_user};").fetchone()
            value_id_group = self.cursor.execute(f"SELECT COUNT(*) FROM {table_users_groups} WHERE id_user={id_user};").fetchone()
            if not value_id_loc and not value_id_group:
                return 0, 0
            return value_id_loc[0], value_id_group[0]
        except Exception as e:
            msg = f"We found problem with the getting lengthes of the locations and groups of the users. Mistake: {e}"
            self.proceed_error(msg)
            return 0, 0

    def delete_poll(self, value_id:int) -> bool:
        """
        Method which is dedicated to removing from the poll coolumns
        Input:  value_id = id of the poll
        Output: remove values from poll column
        """
        try:
            self.cursor.execute(f"DELETE FROM {table_poll} WHERE id=?;", (value_id,))
            self.connection.commit()
            return True
        except Exception as e:
            msg = f'We faced problems with the deleting from the poll table; Mistake: {e}'
            self.proceed_error(msg)
            return False
    
    def delete_poll_group(self, value_id:int) -> bool:
        """
        Method which is dedicated to remove from the poll groups
        Input:  value_id = id of the poll
        Output: removed from the poll_groups table
        """
        try:
            self.cursor.execute(f"DELETE FROM {table_poll_groups} WHERE id_poll=?;", (value_id,))
            self.connection.commit()
            return True
        except Exception as e:
            msg = f"We faced problems with deleting from the poll group table; Mistake: {e}"
            self.proceed_error(msg)
            return False

    def produce_deletion_current_poll(self, value_id:int) -> bool:
        """
        Methodw which is dedicated to produce deletion from the current id
        Input:  value_id = id of the poll
        Output: we removed all values with the
        """
        try:
            self.delete_poll_group(value_id)
            self.delete_poll(value_id)
            return True
        except Exception as e:
            msg = f"We faced problems with the producing of the deletion; Mistake: {e}"
            self.proceed_error(msg)
            return False

    def produce_deletion_previous_values_poll(self) -> bool:
        """
        Method which is dedicated to remove every olda value from the database
        Input:  None
        Output: we removed values which are too old for it
        """
        try:
            value_groups = self.cursor.execute(f"SELECT id from {table_poll} WHERE (julianday('now') - julianday(datetime)) * 24 * 60 > {value_old_default};").fetchall()
            value_groups = [str(f[0]) for f in value_groups]
            value_present = ','.join(value_groups)
            self.cursor.execute(f"DELETE FROM {table_poll_groups} WHERE id_poll IN ({value_present});")
            self.cursor.execute(f"DELETE FROM {table_poll} WHERE id IN ({value_present});")
            self.connection.commit()
            return True
        except Exception as e:
            msg = f"We faced problems with the getting old poll values and deleting them; Mistake: {e}"
            self.proceed_error(msg)
            return False

    def produce_insertion_poll(self, value_list:list, id_user, latitude, longitude) -> bool:
        """
        Method which is dedicated to make basic insertion to the
        Input:  value_list = list with conditions [index, id_group, id_poll]
        Output: boolean value which was previously signed
        """
        try:
            value_id = value_list[0][-1]
            self.cursor.execute(f"INSERT INTO {table_poll}(id, id_user, latitude, longitude) VALUES(?,?,?,?);", (value_id, id_user, latitude, longitude))
            self.connection.commit()
            return True
        except Exception as e:
            msg = f"We faced errors with the execution of insertion to the poll table; Mistake: {e}"
            self.proceed_error(msg)
            return False

    def produce_insertion_poll_group(self, value_list:list) -> bool:
        """
        Method which is dedicated to produce insertion to the poll group
        Input:  value_list = list for the insertion with values [index, id_group, id_poll]
        Output: boolean value which signify that everything is okay
        """
        try:
            self.cursor.executemany(f"INSERT INTO {table_poll_groups}(id_int, id_group, id_poll) VALUES (?, ?, ?);", value_list)
            self.connection.commit()
            return True
        except Exception as e:
            msg = f'We faced problems with multiple group insertion to the database; Mistake: {e}'
            self.proceed_error(msg)
            return False

    def return_poll_id(self, value_id:int) -> set:
        """
        Method which is dedicated to return all necessary values for the poll id 
        Input:  value_id = id of the poll which we would further use
        Output: we get all required values for the sending to the user
        """
        try:
            value_coordinates = self.cursor.execute(f"SELECT id_user, latitude, longitude FROM {table_poll} WHERE id=?;", (value_id,)).fetchall()
            value_lists = self.cursor.execute(f"SELECT id_group FROM {table_poll_groups} WHERE id_poll=?;", (value_id,)).fetchall()
            value_coordinates = value_coordinates[-1] if value_coordinates else []
            value_lists = [f[0] for f in value_lists] if value_lists else []
            return value_coordinates, value_lists
        except Exception as e:
            msg = f"We faced problems with getting values from the database via poll id; Mistake: {e}"
            self.proceed_error(msg)
            return [], []

    def produce_multiple_insertion_poll(self, value_list:list, chat_id:int, latitude, longitude) -> bool:
        """
        Method which is dedicated to insert values for the quizez
        Input:  value_list = list with values of the [index, id_group, id_poll]
                latitude = coordinate value of latitude
                longitude = coordinate value of longitude
        Output: we inserted all values and previously checked
        """
        try:
            self.produce_deletion_previous_values_poll()
            self.produce_insertion_poll(value_list, chat_id, latitude, longitude)
            self.produce_insertion_poll_group(value_list)
            return True
        except Exception as e:
            msg = f"We faced problems with insertion values to the {table_poll} and {table_poll_groups}; Mistake: {e}"
            self.proceed_error(msg)
            return False

    def produce_values(self) -> None:
        """
        Method which is dedicated to create the database for the bot usage
        Input:  Nothing
        Output: we sucessfully created database with the tables
        """
        self.create_folder(self.folder_config)
        self.name_db = os.path.join(self.folder_config, name_db)
        if not os.path.exists(self.name_db) or not os.path.isfile(self.name_db):
            self.connection = sqlite3.connect(self.name_db, check_same_thread=False)
            self.cursor = self.connection.cursor()
            self.cursor.execute(f""" 
                CREATE TABLE IF NOT EXISTS {table_users}(
                    id INTEGER PRIMARY KEY,
                    name_first TEXT,
                    name_last TEXT,
                    nickname TEXT
                );""")
            self.cursor.execute(f""" 
                CREATE TABLE IF NOT EXISTS {table_locations}(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name_location TEXT,
                    latitude TEXT,
                    longitude TEXT
                );""")
            self.cursor.execute(f""" 
                CREATE TABLE IF NOT EXISTS {table_groups}(
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    date_value DATETIME DEFAULT CURRENT_TIMESTAMP
                );""")
            self.cursor.execute(f""" 
                CREATE TABLE IF NOT EXISTS {table_users_groups}(
                    id_user INTEGER,
                    id_group INTEGER,
                    PRIMARY KEY (id_user, id_group),
                    FOREIGN KEY (id_user) REFERENCES {table_users} (id)
                        ON DELETE CASCADE 
                        ON UPDATE NO ACTION,
                    FOREIGN KEY (id_group) REFERENCES {table_groups} (id)
                        ON DELETE CASCADE 
                        ON UPDATE NO ACTION
                );""")
            self.cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {table_groups_selected}(
                    id_user INTEGER,
                    id_group INTEGER,
                    PRIMARY KEY (id_user, id_group),
                    FOREIGN KEY (id_user) REFERENCES {table_users} (id)
                        ON DELETE CASCADE 
                        ON UPDATE NO ACTION,
                    FOREIGN KEY (id_group) REFERENCES {table_groups} (id)
                        ON DELETE CASCADE 
                        ON UPDATE NO ACTION
                );""")
            self.cursor.execute(f""" 
                CREATE TABLE IF NOT EXISTS {table_users_locations}(
                    id_user INTEGER,
                    id_location INTEGER,
                    PRIMARY KEY (id_user, id_location),
                    FOREIGN KEY (id_user) REFERENCES {table_users} (id)
                        ON DELETE CASCADE 
                        ON UPDATE NO ACTION,
                    FOREIGN KEY (id_location) REFERENCES {table_locations} (id)
                        ON DELETE CASCADE 
                        ON UPDATE NO ACTION
                );""")
            self.cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {table_users_settings}(
                    id_user INTEGER PRIMARY KEY,
                    text_sending TEXT DEFAULT "{entrance_bot_usage}",
                    text_minutes INTEGER DEFAULT {value_message_default},
                    name_default TEXT DEFAULT '{name_loc_default}',
                    name_default_boolean BOOLEAN DEFAULT TRUE,
                    name_default_audio TEXT,
                    audio_boolean BOOLEAN DEFAULT FALSE,
                    name_default_video TEXT,
                    video_boolean BOOLEAN DEFAULT FALSE,
                    message_priority INTEGER DEFAULT {value_message_selection_default}
                );""")
            self.cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {table_user_group_connect}(
                    id_user INTEGER,
                    id_group INTEGER,
                    text_message TEXT DEFAULT "{name_join_default}",
                    PRIMARY KEY(id_user, id_group),
                    FOREIGN KEY (id_user) REFERENCES {table_users} (id)
                        ON DELETE CASCADE 
                        ON UPDATE NO ACTION,
                    FOREIGN KEY (id_group) REFERENCES {table_groups} (id)
                        ON DELETE CASCADE 
                        ON UPDATE NO ACTION
                );""")
            self.cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {table_poll}(
                    id INTEGER,
                    id_user INTEGER,
                    latitude TEXT,
                    longitude TEXT,
                    datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (id)
                );""")
            self.cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {table_poll_groups}(
                    id_int INTEGER,
                    id_poll INTEGER,
                    id_group INTEGER,
                    PRIMARY KEY (id_poll, id_group),
                    FOREIGN KEY (id_poll) REFERENCES {table_poll} (id)
                        ON DELETE CASCADE 
                        ON UPDATE NO ACTION,
                    FOREIGN KEY (id_group) REFERENCES {table_groups} (id)
                        ON DELETE CASCADE 
                        ON UPDATE NO ACTION
                );""")
            self.connection.commit()
        else:
            self.create_connection()