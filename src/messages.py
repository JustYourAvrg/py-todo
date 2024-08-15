import customtkinter as ctk


class Message:
    def showerror(title: str, message: str):
        err = ctk.CTk()
        err.title(title)
        err.geometry("200x200")
        err.resizable(0, 0)

        err.grid_rowconfigure(0, weight=1)
        err.grid_columnconfigure(0, weight=1)
        err.grid_propagate(0)

        msg = ctk.CTkLabel(err, text=message, wraplength=180)
        msg.grid(row=0, column=0)

        err.mainloop()


    def askyesno(title: str, message: str):
        res = None

        yn = ctk.CTk()
        yn.title(title)
        yn.geometry("200x200")
        yn.resizable(0, 0)

        yn.grid_rowconfigure((0, 1), weight=1)
        yn.grid_columnconfigure((0, 1), weight=1)
        yn.grid_propagate(0)

        msg = ctk.CTkLabel(yn, text=message, wraplength=180)
        msg.grid(row=0, column=0, sticky='nsew', columnspan=2)

        def yes_action():
            nonlocal res
            yn.quit()
            yn.destroy()
            res = True

        def no_action():
            nonlocal res
            yn.quit()
            yn.destroy()
            res = False

        yes_btn = ctk.CTkButton(yn, text="YES", fg_color="#66FF66", text_color="#000000", font=ctk.CTkFont(weight='bold'), width=40, command=yes_action)
        yes_btn.grid(row=1, column=0)

        no_btn = ctk.CTkButton(yn, text="NO", fg_color="#FF6666", text_color="#000000", font=ctk.CTkFont(weight='bold'), width=40, command=no_action)
        no_btn.grid(row=1, column=1)

        yn.mainloop()
        return res