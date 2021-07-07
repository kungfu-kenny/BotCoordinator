import os
import sqlite3
from sqlite3.dbapi2 import Connection
import sqlite3
from config import (name_db,
                    folder_config,
                    table_users,
                    table_groups,
                    table_locations,
                    table_users_groups,
                    table_users_locations)


class DataUsage:
    """
    class which is dedicated to produce the values of the 
    """
    def __init__(self) -> None:
        self.folder_current = os.getcwd()
        self.folder_config = os.path.join(self.folder_current, folder_config)
        self.create_folder = lambda x: os.path.exists(x) or os.mkdir(x)
        self.produce_values()

    def create_connection(self) -> None:
        """
        Method which is dedicated to produce the connection of the 
        Input:  None
        Output: we created the database
        """
        try:
            self.create_folder(self.folder_config)
            self.connection = sqlite3.connect(self.name_db)
            self.cursor = self.connection.cursor()
        except Exception as e:
            print(f'We faced problems with the connection. Reason: {e}')

    def close_connection(self) -> None:
        """
        Method which is dedicated to close the 
        Input:  None
        Output: we closed the connection to the database
        """
        self.connection.close()

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
            print(f'We found problems with checking values of the previous insertion, mistake: {e}')

    def get_current_id(self) -> int:
        """
        Method which is dedicated to manually return values from the database manually
        Input:  None
        Output: we successfully returned last id of the coordinate
        """
        try:
            return self.cursor.execute(f"SELECT MAX(id) FROM {table_locations};").fetchone()
        except Exception as e:
            print('We faced some problems with the getting last id value')
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
            #TODO create the insertion to the user if it is required
            id_user, username, name_first, name_last = id_list
            if not self.get_user_values(id_user):
                self.insert_username(id_user, username, name_first, name_last)
            self.cursor.execute(f"INSERT INTO {table_locations} (name_location, latitude, longitude) VALUES (?, ?, ?);", 
                                (name_location, latitude, longitude))
            self.cursor.execute(f"INSERT INTO {table_users_locations} (id_user, id_location) VALUES (?, ?);", (id_user, self.cursor.lastrowid))
            return True
        except Exception as e:
            print(f'We faced problems with the performing of the operating of the location inserting. Mistake: {e}')
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
            return True
        except Exception as e:
            print('We faced problem with inserting values within the database')
            return False

    def produce_values(self) -> None:
        """
        Method which is dedicated to create the database for the bot usage
        Input:  Nothing
        Output: we sucessfully created database with the tables
        """
        self.create_folder(self.folder_config)
        self.name_db = os.path.join(self.folder_config, name_db)
        # if not os.path.exists(self.name_db) or not os.path.isfile(self.name_db):
        connection = sqlite3.connect(self.name_db)
        connection_cursor = connection.cursor()
        connection_cursor.execute(f""" 
            CREATE TABLE IF NOT EXISTS {table_users}(
                id INTEGER PRIMARY KEY,
                name_first TEXT,
                name_last TEXT,
                nickname TEXT
            );
            CREATE TABLE IF NOT EXISTS {table_locations}(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name_location TEXT,
                latitude TEXT,
                longitude TEXT
            );
            CREATE TABLE IF NOT EXISTS {table_groups}(
                id INTEGER PRIMARY KEY,
                name TEXT
            );
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
            );
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
        connection.commit()
        connection.close()
