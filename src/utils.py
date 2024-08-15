import customtkinter as ctk
import sqlite3

from tabulate import tabulate
from typing import Literal


class Utils:
    def __init__(self, db_file_path):
        # Connect to the database
        self.db = sqlite3.connect(db_file_path)
        self.cur = self.db.cursor()
        
        # Create the tables for the database
        self.create_tables()


    def create_tables(self):
        """
        Creates the 'todos' table if it doesn't exist.
        """

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            completed BOOLEAN,
            priority INTEGER,
            due_date DATETIME,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)
        """)
    

    def add_todo(self, title: str=None, desc: str=None, complete: bool=False, priority: int=1, due_date: str=None, bypassError: bool=False):
        """
        Add a new todo task to the database.
        Parameters:
        - title (str): The title of the todo task.
        - desc (str): The description of the todo task.
        - complete (bool): The completion status of the todo task. Default is False.
        - priority (int): The priority level of the todo task. Default is 1.
        - due_date (str): The due date of the todo task.
        - bypassError (bool): Flag to bypass error checking. Default is False.
        Returns:
        - Exception: If an error occurs during the execution of the function.
        """
        try:
            if not bypassError:
                if self.cur.execute("SELECT title FROM todos WHERE title = ?", (title,)).fetchone():
                    raise(Exception("ERROR"))

            self.cur.execute("INSERT INTO todos (title, description, completed, priority, due_date) VALUES(?, ?, ?, ?, ?)", 
            (title, desc, complete, priority, due_date))
            self.db.commit()

        except Exception as e:
            return str(e)

    
    def get_todos(self, sort_by: Literal["alphabetically", "time_added", "time_added_reversed", "importance"]="importance"):
        """
        Retrieve todos from the database and sort them based on the specified criteria.

        Args:
            sort_by (Literal["alphabetically", "time_added", "time_added_reversed", "importance"]): 
                The criteria to sort the todos. Defaults to "importance".

        Returns:
            list: A list of todos sorted based on the specified criteria.

        Raises:
            Exception: If there is an error retrieving the todos from the database.
        """
        try:
            todo_data = self.cur.execute("SELECT * FROM todos").fetchall()

            if sort_by == 'alphabetically':
                todo_data = sorted(todo_data, key=lambda x: x[1])
            elif sort_by == 'time_added':
                todo_data = sorted(todo_data, key=lambda x: x[6])
            elif sort_by == 'time_added_reversed':
                todo_data = sorted(todo_data, key=lambda x: x[6], reverse=True)
            elif sort_by == 'importance':
                todo_data = sorted(todo_data, key=lambda x: x[4], reverse=True)

            return todo_data
        
        except Exception as e:
            return e
    

    def edit_todo(self, id: int, title: str=None, desc: str=None, complete: bool=None, priority: int=None, due_date: str=None):
        """
        Edit a todo item in the database.
        Args:
            id (int): The ID of the todo item to be edited.
            title (str, optional): The new title for the todo item. Defaults to None.
            desc (str, optional): The new description for the todo item. Defaults to None.
            complete (bool, optional): The new completion status for the todo item. Defaults to None.
            priority (int, optional): The new priority for the todo item. Defaults to None.
            due_date (str, optional): The new due date for the todo item. Defaults to None.
        Returns:
            Exception or None: If an error occurs during the update, an Exception object is returned. Otherwise, None is returned.
        """
        try:
            old_data = self.cur.execute("SELECT * FROM todos WHERE id = ?", (id,)).fetchall()[0]
            
            self.cur.execute("""UPDATE todos 
                SET title = ?, description = ?, completed = ?, priority = ?, due_date = ?
                WHERE id = ?""", 
            (
                old_data[1] if title is None else title,
                old_data[2] if desc is None else desc,
                old_data[3] if complete is None else complete,
                old_data[4] if priority is None else priority,
                old_data[5] if due_date is None else due_date,
                id
            ))

            self.db.commit()

        except Exception as e:
            return e


    def delete_todo(self, todo_index=None):
        """
        Deletes a todo item from the database.
        Parameters:
        - todo_index (int): The index of the todo item to be deleted.
        Raises:
        - Exception: If an error occurs while deleting the todo item.
        Returns:
        - None
        """

        try:
            self.cur.execute("DELETE FROM todos WHERE id = ?", (todo_index,))
            self.db.commit()

        except Exception as e:
            return e