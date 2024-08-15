import customtkinter as ctk
import os
import datetime

from utils import Utils
from PIL import Image
from messages import Message
from tkinter import Spinbox


class Gui:
    def __init__(self):
        # Initialize the Utils class and get the current year
        self.utils = Utils(db_file_path=f"database.db")
        self.cur_date = datetime.datetime.now().year

        # Get the image paths
        self.image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.complete_btn_img = ctk.CTkImage(Image.open(os.path.join(self.image_path, "checked.png")))
        self.edit_btn_img = ctk.CTkImage(Image.open(os.path.join(self.image_path, "edit.png")))
        self.delete_btn_img = ctk.CTkImage(Image.open(os.path.join(self.image_path, "delete.png")))
        self.un_complete_btn_img = ctk.CTkImage(Image.open(os.path.join(self.image_path, "uncomplete.png")))
        self.add_btn_img = ctk.CTkImage(Image.open(os.path.join(self.image_path, "add.png")), size=(115, 115))

        # Width and height for the GUI
        self.width, self.height = 1080, 600

        # Initialize the window, and configure the rows and columns
        self.root = ctk.CTk()
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.resizable(0, 0)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
        # Nav frame
        self.nav_frame = ctk.CTkFrame(self.root, width=200, fg_color="#161616", corner_radius=0)
        self.nav_frame.grid(row=0, column=0, sticky='nsw')
        self.nav_frame.grid_rowconfigure((0, 1, 2), weight=0)
        self.nav_frame.grid_rowconfigure(3, weight=1)

        # Nav frame label
        self.nav_label = ctk.CTkLabel(self.nav_frame, text="Py | Todo", corner_radius=0, font=ctk.CTkFont(size=18, weight='bold'))
        self.nav_label.grid(row=0, column=0, sticky='n', pady=(20, 20))

        # Home Tab nav-button
        self.home_tab_toggle = ctk.CTkButton(self.nav_frame, 
                                                  text="Home", 
                                                  command=lambda frame="home": self.select_frame(name=frame), 
                                                  corner_radius=0, 
                                                  fg_color="#1e1e1e", 
                                                  hover_color="#2c2c2c",
                                                  height=50,
                                                  font=ctk.CTkFont(size=16))
        self.home_tab_toggle.grid(row=1, column=0, sticky='n')

        # Completed Tab nav-button
        self.completed_tab_toggle = ctk.CTkButton(self.nav_frame, 
                                                  text="Completed", 
                                                  command=lambda frame="completed_tab": self.select_frame(name=frame), 
                                                  corner_radius=0, 
                                                  fg_color="#1e1e1e", 
                                                  hover_color="#2c2c2c",
                                                  height=50,
                                                  font=ctk.CTkFont(size=16)
                                                  )
        self.completed_tab_toggle.grid(row=2, column=0, sticky='n')

        # Select type of sorting
        self.select_sorting = ctk.CTkOptionMenu(self.nav_frame, values=["importance", "alphabetically", "time_added", "time_added_reversed"], fg_color="#1e1e1e", button_color="#141414", button_hover_color="#1c1c1c")
        self.select_sorting.grid(row=3, column=0, sticky='s')
        self.select_sorting.configure(command=lambda v=self.select_sorting.get(): self.refresh_todo_frame(sort_by=v))
        self.select_sorting.grid_propagate(0)
        
        # Home frame
        self.home_frame = ctk.CTkScrollableFrame(self.root, corner_radius=0, fg_color="#141414")
        self.home_frame.grid_rowconfigure(0, weight=0)
        self.home_frame.grid_columnconfigure((0, 1, 2), weight=0)
        
        # Completed frame
        self.completed_frame = ctk.CTkFrame(self.root, corner_radius=0, fg_color="#141414")

        # Get the todos and select the home frame
        self.refresh_todo_frame()
        self.select_frame("home")

    
    def get_completed_todos(self):
        # Destroy all child widgets inside the completed_frame
        for child in self.completed_frame.winfo_children():
            child.destroy()
        
        # Get all the todos and sort them by "importance"
        self.fetched_todos = self.utils.get_todos(sort_by='importance')
        cur_row = 0

        # For index and todo in the fetched todos, setup the todo frame with the todo details
        for i, todo in enumerate(self.fetched_todos, start=1):
            # If todo[3] ( completed = True )
            if todo[3]:
                # todo frame
                todo_frame = ctk.CTkFrame(self.completed_frame, corner_radius=15, fg_color="#1e1e1e", height=300)
                todo_frame.grid(row=0 if i < 4 else cur_row + 1, column=i % 4, padx=10, pady=10, sticky='w')
                todo_frame.grid_rowconfigure((0, 1), weight=0)
                todo_frame.grid_rowconfigure(2, weight=1)

                # Frame to hold task and priority
                top_frame = ctk.CTkFrame(todo_frame, fg_color="#1e1e1e", height=30)
                top_frame.grid(row=0, column=0, pady=5)
                top_frame.grid_rowconfigure(0, weight=1)
                top_frame.grid_columnconfigure((0, 1), weight=2)
                top_frame.grid_propagate(0)

                # Todo Task 
                task = ctk.CTkLabel(top_frame, text=todo[1], corner_radius=15, bg_color="#1e1e1e", text_color="#FFFFFF")
                task.grid(row=0, column=0, sticky='ew', pady=5, padx=5)

                # Priority
                priority = ctk.CTkLabel(top_frame, 
                                        text=f"{'low' if todo[4] == 1 else 'medium' if todo[4] == 2 else 'high' if todo[4] == 3 else ''}", 
                                        text_color="#FF0000" if todo[4] == 3 else "#FFA500" if todo[4] == 2 else "#FFFF00" if todo[4] == 1 else "")
                priority.grid(row=0, column=1, sticky='ew', pady=5, padx=5)

                # Description
                description = ctk.CTkTextbox(todo_frame, fg_color="#1b1c1b", wrap=ctk.WORD, text_color="#e0e0e0")
                description.grid(row=1, column=0, pady=5, padx=10, sticky='nsew')
                description.insert(ctk.END, todo[2])
                description.configure(state='disabled')
                
                # Due-date
                due_date = ctk.CTkLabel(todo_frame, text=f"Due by - {todo[5]}", text_color="#A9A9A9")
                due_date.grid(row=2, column=0, pady=5, padx=10)

                # Nav bar for the completed todos
                completed_frame_todo_nav = ctk.CTkFrame(todo_frame, height=28, corner_radius=0)
                completed_frame_todo_nav.grid(row=3, column=0, sticky='nsew')
                completed_frame_todo_nav.grid_rowconfigure(0, weight=1)
                completed_frame_todo_nav.grid_columnconfigure((0, 1), weight=1)
                completed_frame_todo_nav.grid_propagate(0)

                # Mark todos un-complete
                un_complete_button = ctk.CTkButton(completed_frame_todo_nav, image=self.un_complete_btn_img, text="", fg_color="transparent", hover_color="#1c1c1c", corner_radius=0, cursor='hand2')
                un_complete_button.grid(row=3, column=0, sticky='nsew')
                un_complete_button.bind("<Button-1>", lambda event, id=todo[0], todo_task=todo[1]: self.uncomplete_todo(event, id, todo_task))

                # Delete the todo
                delete_btn = ctk.CTkButton(completed_frame_todo_nav, image=self.delete_btn_img, text="", fg_color="transparent", hover_color="#1c1c1c", corner_radius=0, cursor='hand2')
                delete_btn.grid(row=3, column=1, sticky='nsew')
                delete_btn.bind("<Button-1>", lambda event, id=todo[0], todo_task=todo[1]: self.delete_todo(event, id, todo_task, is_completed_frame=True))


    def refresh_todo_frame(self, sort_by: str="importance"):
        for child in self.home_frame.winfo_children():
            child.destroy()

        self.add_todo_button_frame = ctk.CTkFrame(self.home_frame, height=300, fg_color="transparent", corner_radius=15)
        self.add_todo_button_frame.grid_rowconfigure(0, weight=1)
        self.add_todo_button_frame.grid_columnconfigure(0, weight=1)
        self.add_todo_button_frame.grid_propagate(0)
        self.add_todo_button_frame.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        self.add_todo_btn = ctk.CTkButton(self.add_todo_button_frame, image=self.add_btn_img, fg_color="transparent", hover_color="#1c1c1c", text="", corner_radius=15, cursor='hand2')
        self.add_todo_btn.grid(row=0, column=0, sticky='nsew', padx=3, pady=3)

        self.add_todo_btn.bind("<Button-1>", self.on_add_todo_click)

        self.fetched_todos = self.utils.get_todos(sort_by=sort_by)
        cur_row = 0
        for i, todo in enumerate(self.fetched_todos, start=1):
            if not todo[3]:
                todo_frame = ctk.CTkFrame(self.home_frame, corner_radius=15, fg_color="#1e1e1e", height=300)
                todo_frame.grid(row=0 if i < 4 else cur_row + 1, column=i % 4, padx=10, pady=10, sticky='w')
                todo_frame.grid_rowconfigure((0, 1), weight=0)
                todo_frame.grid_rowconfigure(2, weight=1)

                # Frame to hold task and priority
                top_frame = ctk.CTkFrame(todo_frame, fg_color="#1e1e1e", height=30)
                top_frame.grid(row=0, column=0, pady=5)
                top_frame.grid_rowconfigure(0, weight=1)
                top_frame.grid_columnconfigure((0, 1), weight=2)
                top_frame.grid_propagate(0)

                # Todo Task 
                task = ctk.CTkLabel(top_frame, text=todo[1], corner_radius=15, bg_color="#1e1e1e", text_color="#FFFFFF")
                task.grid(row=0, column=0, sticky='ew', pady=5, padx=5)

                # Priority
                priority = ctk.CTkLabel(top_frame, 
                                        text=f"{'low' if todo[4] == 1 else 'medium' if todo[4] == 2 else 'high' if todo[4] == 3 else ''}", 
                                        text_color="#FF0000" if todo[4] == 3 else "#FFA500" if todo[4] == 2 else "#FFFF00" if todo[4] == 1 else "")
                priority.grid(row=0, column=1, sticky='ew', pady=5, padx=5)

                # Description
                description = ctk.CTkTextbox(todo_frame, fg_color="#1b1c1b", wrap=ctk.WORD, text_color="#e0e0e0")
                description.grid(row=1, column=0, pady=5, padx=10, sticky='nsew')
                description.insert(ctk.END, todo[2])
                description.configure(state='disabled')
                
                # Due-date
                due_date = ctk.CTkLabel(todo_frame, text=f"Due by - {todo[5]}", text_color="#A9A9A9")
                due_date.grid(row=2, column=0, pady=5, padx=10)

                # Nav bar for the todo frame
                todo_nav = ctk.CTkFrame(todo_frame, height=30, corner_radius=0)
                todo_nav.grid(row=3, column=0, sticky='nsew')
                todo_nav.grid_rowconfigure(0, weight=1)
                todo_nav.grid_columnconfigure((0, 1, 2), weight=1)
                todo_nav.grid_propagate(0)

                # Mark the todo as completed
                complete_btn = ctk.CTkButton(todo_nav, image=self.complete_btn_img, text="", fg_color="transparent", hover_color="#1c1c1c", corner_radius=0, cursor='hand2')
                complete_btn.grid(row=0, column=0, sticky='nsew')
                complete_btn.bind("<Button-1>", command=lambda event, id=todo[0], todo_task=todo[1]: self.complete_todo(event, id, todo_task))

                # Edit the todo
                edit_btn = ctk.CTkButton(todo_nav, image=self.edit_btn_img, text="", fg_color="transparent", hover_color="#1c1c1c", corner_radius=0, cursor='hand2')
                edit_btn.grid(row=0, column=1, sticky='nsew')
                edit_btn.bind("<Button-1>", lambda event, id=todo[0], todo_task=todo[1], todo_desc=todo[2]: self.edit_todo(event, id, todo_task, todo_desc))

                # Delete the todo
                delete_btn = ctk.CTkButton(todo_nav, image=self.delete_btn_img, text="", fg_color="transparent", hover_color="#1c1c1c", corner_radius=0, cursor='hand2')
                delete_btn.grid(row=0, column=2, sticky='nsew')
                delete_btn.bind("<Button-1>", lambda event, id=todo[0], todo_task=todo[1]: self.delete_todo(event, id, todo_task))


    def complete_todo(self, e, id, todo_task):
        val = Message.askyesno(title=todo_task, message=f"Would you like to mark the todo {todo_task} as complete?")

        if val:
            self.utils.edit_todo(id=id, complete=True)
            self.refresh_todo_frame()
    

    def uncomplete_todo(self, e, id, task):
        val = Message.askyesno(title=task, message=f"Would you like to unmark this todo {task} as complete?")

        if val:
            self.utils.edit_todo(id=id, complete=False)
            self.get_completed_todos()


    def edit_todo(self, e, id, todo_task, todo_desc):
            def confirm_edit():
                todo = None if task.get() == "" else task.get()
                desc = None if description.get(0.0, ctk.END) == "" else description.get(0.0, ctk.END)
                priority = 1 if task_priority.get() == 'low' else 2 if task_priority.get() == 'medium' else 3 if task_priority.get() == 'high' else None
                day = get_day.get()
                month = get_month.get()
                year = None if get_year.get() == "" else get_year.get()
                due_by = f"{day}-{month}-{year}"

                if len(str(year)) < 4 or len(str(year)) > 5 or year.isalpha():
                    Message.showerror("ERROR", "Please enter a valid year (e.g: 2025)")
                    edit.quit()
                    return
                
                if todo and desc and priority and day and month and year != None:
                    val = Message.askyesno(title=todo_task, message=f"Are you sure you want to edit the todo: {todo_task}?")
                    if val:
                        self.utils.edit_todo(id, title=todo, desc=desc, priority=priority, due_date=due_by)
                        self.refresh_todo_frame()
                else:
                    Message.showerror("ERROR", "Please fill all forms")

                edit.quit()
                edit.destroy()


            edit = ctk.CTk()
            edit.geometry("275x300")
            edit.resizable(False, False)

            edit_frame = ctk.CTkFrame(edit, width=275, height=300, corner_radius=0)
            edit_frame.grid(row=0, column=0, columnspan=2, sticky='nsew')
            edit_frame.grid_rowconfigure(1, weight=1)
            edit_frame.grid_columnconfigure((0, 1), weight=1)
            edit_frame.grid_propagate(0)

            # Task
            task = ctk.CTkEntry(edit_frame, placeholder_text=todo_task)
            task.grid(row=0, column=0, padx=5, pady=(10, 0))
            
            # Priority
            task_priority = ctk.CTkOptionMenu(edit_frame, values=["Set priority", "low", "medium", "high"], button_color="#151515", fg_color="#1c1c1c", button_hover_color="#232323")
            task_priority.grid(row=0, column=1, padx=5, pady=(10, 0))

            # Description
            description = ctk.CTkTextbox(edit_frame, wrap=ctk.WORD, fg_color="#131313")
            description.grid(row=1, column=0, padx=10, pady=10, sticky='nsew', columnspan=2)
            description.insert(ctk.END, todo_desc)

            # Due Date frame
            due_date_frame = ctk.CTkFrame(edit_frame, corner_radius=0)
            due_date_frame.grid(row=2, column=0, columnspan=4, sticky='ew')
            due_date_frame.grid_columnconfigure((0, 1, 2, 3), weight=2)

            # Due date
            get_day = ctk.CTkOptionMenu(due_date_frame, values=[str(x+1) for x in range(31)], fg_color="#131313", button_color="#1e1e1e", button_hover_color="#1c1c1c")
            get_day.grid(row=0, column=0, padx=3)

            get_month = ctk.CTkOptionMenu(due_date_frame, values=[str(f"{f"0{x+1}" if x+1 < 10 else x+1}") for x in range(12)], fg_color="#131313", button_color="#1e1e1e", button_hover_color="#1c1c1c")
            get_month.grid(row=0, column=1, padx=3)

            get_year = Spinbox(
                due_date_frame,
                from_=self.cur_date,
                to=self.cur_date+200,
                width=12,
                foreground="#FFFFFF",
                background="#131313",
                buttonbackground="#1e1e1e",
                borderwidth=0,
                font=ctk.CTkFont(size=12)
            )
            get_year.grid(row=0, column=3, padx=3, sticky='nsew')

            # Submit button
            edit_btn = ctk.CTkButton(due_date_frame, text="Edit", fg_color="#131313", hover_color="#151515", cursor="hand2", command=confirm_edit, width=30)
            edit_btn.grid(row=0, column=4, padx=5, pady=5)

            edit.mainloop()

    
    #TODO: Add a confirmation message
    def delete_todo(self, e, id, todo_task, is_completed_frame=False):
        val = Message.askyesno("DELETE", f"Are you sure you want to delete the todo: {todo_task}")

        if val:
            self.utils.delete_todo(todo_index=id)
            if is_completed_frame:
                self.get_completed_todos()
            else:
                self.refresh_todo_frame()

    
    def select_frame(self, name=str):
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
            self.refresh_todo_frame()
        else:
            self.home_frame.grid_remove()
        
        if name == "completed_tab":
            self.completed_frame.grid(row=0, column=1, sticky="nsew")
            self.get_completed_todos()
        else:
            self.completed_frame.grid_remove()
            

    def on_add_todo_click(self, e):
        try:
            def confirm_add_todo():
                title = None if task.get() == "" else task.get()
                desc = None if description.get(0.0, ctk.END) == "" else description.get(0.0, ctk.END)
                priority = 1 if task_priority.get() == 'low' else 2 if task_priority.get() == 'medium' else 3 if task_priority.get() == 'high' else None
                day = get_day.get()
                month = get_month.get()
                year = None if get_year.get() == "" else get_year.get()
                due_by = f"{day}-{month}-{year}"

                if len(str(year)) < 4 or len(str(year)) > 5 or year.isalpha():
                    Message.showerror("ERROR", "Please enter a valid year (e.g: 2025)")
                    add_todo.quit()
                    return

                if title and desc and day and month and year and priority != None:
                    attempt = self.utils.add_todo(title=title, desc=desc, priority=priority, due_date=due_by)
                    print(attempt)
                    if attempt == "ERROR":
                        val = Message.askyesno(title="Duplicate todo", message=f'You already have a todo named {title} are you sure you want to add another?')
                        if val:
                           self.utils.add_todo(title=title, desc=desc, priority=priority, due_date=due_by, bypassError=True)

                    self.refresh_todo_frame()
                    add_todo.quit()
                    add_todo.destroy()
                else:
                    Message.showerror("ERROR", "Please fill all forms")

            add_todo = ctk.CTk()
            add_todo.geometry("275x300")
            add_todo.resizable(False, False)

            add_todo_frame = ctk.CTkFrame(add_todo, width=275, height=300, corner_radius=0)
            add_todo_frame.grid(row=0, column=0, columnspan=2, sticky='nsew')
            add_todo_frame.grid_rowconfigure(1, weight=1)
            add_todo_frame.grid_columnconfigure((0, 1), weight=1)
            add_todo_frame.grid_propagate(0)

            # Task
            task = ctk.CTkEntry(add_todo_frame, placeholder_text="Task...")
            task.grid(row=0, column=0, padx=5, pady=(10, 0))
            
            # Priority
            task_priority = ctk.CTkOptionMenu(add_todo_frame, values=["Set priority", "low", "medium", "high"], button_color="#151515", fg_color="#1c1c1c", button_hover_color="#232323")
            task_priority.grid(row=0, column=1, padx=5, pady=(10, 0))

            # Description
            description = ctk.CTkTextbox(add_todo_frame, wrap=ctk.WORD, fg_color="#131313")
            description.grid(row=1, column=0, padx=10, pady=10, sticky='nsew', columnspan=2)
            description.insert(ctk.END, "Description...")

            # Due Date frame
            due_date_frame = ctk.CTkFrame(add_todo_frame, corner_radius=0)
            due_date_frame.grid(row=2, column=0, columnspan=4, sticky='ew')
            due_date_frame.grid_columnconfigure((0, 1, 2, 3), weight=2)

            # Due date
            get_day = ctk.CTkOptionMenu(due_date_frame, values=[str(x+1) for x in range(31)], fg_color="#131313", button_color="#1e1e1e", button_hover_color="#1c1c1c")
            get_day.grid(row=0, column=0, padx=3)

            get_month = ctk.CTkOptionMenu(due_date_frame, values=[str(f"{f"0{x+1}" if x+1 < 10 else x+1}") for x in range(12)], fg_color="#131313", button_color="#1e1e1e", button_hover_color="#1c1c1c")
            get_month.grid(row=0, column=1, padx=3)

            get_year = Spinbox(
                due_date_frame,
                from_=self.cur_date,
                to=self.cur_date+200,
                width=12,
                foreground="#FFFFFF",
                background="#131313",
                buttonbackground="#1e1e1e",
                borderwidth=0,
                font=ctk.CTkFont(size=12)
            )
            get_year.grid(row=0, column=3, padx=3, pady=5, sticky='nsew')

            # Submit button
            add_todo_btn = ctk.CTkButton(due_date_frame, text="Add", fg_color="#131313", hover_color="#151515", cursor="hand2", command=confirm_add_todo, width=30)
            add_todo_btn.grid(row=0, column=4, padx=5, pady=5)

            add_todo.mainloop()
        
        except Exception as e:
            print(e)


if __name__ == "__main__":
    gui = Gui()
    gui.root.mainloop()