from tkinter import *
import hashlib
import os
from tkinter import messagebox
from tkinter.ttk import Separator, Treeview
from tkinter.simpledialog import askstring
import json
import re

db_name = "Database.json"

def read_data_from_database(database):
    with open(database) as json_file:
        data = json.load(json_file)
    return data

def write_data_to_database(database, data_to_be_written):
    with open(database, "w") as f_db:
        json.dump(data_to_be_written, f_db)


class User_Profile(Tk):

    def close_window(self):
        self.destroy()
    
    def change_password(self, old_pass, new_password):
        if os.path.exists(db_name):
            list_of_users = read_data_from_database(db_name)
            for user in list_of_users:
                if user["username"] == self.__username:
                    if user["password"] !=old_pass:
                        #Wrong pass
                        messagebox.showwarning("Programm info","Wrong old password!", master=self)
                    else:
                        #Correct pass 
                        if user["password_limit"]:
                            if not re.search("^[a-zA-ZА-Яа-яЁё0-9]+$", new_password):
                                #Dont submit pattern 
                                messagebox.showwarning("Program info", "Password must contain lowercase and uppercase Latin letters, numbers and Cyrillic characters!", master=self)  
                                break
                        user["password"] = (hashlib.md5(new_password.encode()).hexdigest())
                        messagebox.showinfo("Programm info","Password changed!", master=self)
                        self.old_password_entry.delete(0, 'end')
                        self.new_password_entry1.delete(0, 'end')
                        self.new_password_entry2.delete(0, 'end')
                        write_data_to_database(db_name, list_of_users)
                    break # Changed!!!!!
        else:
            messagebox.showerror("Programm info","Problem with database!", master=self)

    def get_passwords_from_inputs(self):
        npsswe1 = self.new_password_entry1.get()
        npsswe2 = self.new_password_entry2.get()
        if npsswe1 =="" or npsswe2 == "":
            messagebox.showinfo("Program info", "Please fill required inputs!", master=self)
        else:
            if npsswe1 != npsswe2:
                messagebox.showinfo("Program info", "Your new password must be the same!", master=self)
            else:
                self.change_password((hashlib.md5(self.old_password_entry.get().encode()).hexdigest()), npsswe1)

    def create_widgets(self):
        welcome_message = "Hello dear " + self.__username +"!\nThis is your personal page."
        
        greeting_label = Label(self, text=welcome_message, fg="#1C1C1C", font="Arial 14")
        greeting_label.place(x=150, y=5)

        separator = Separator(self, orient='horizontal')
        separator.place(width=460, x=20, y=80)

        instruction_label = Label(self, text="Here u can change your password!", fg="#1C1C1C", font="Arial 14")
        instruction_label.place(x=120, y=90)

        old_password_label = Label(self, text="Old password * :", fg="#1C1C1C", font="Arial 11")
        old_password_label.place(x=20, y=140)
         
        self.old_password_entry = Entry(self, width=30, font='Arial 13', show="●")
        self.old_password_entry.place(x=180, y=140, width=250)
        def show_tip_for_old_password():
             messagebox.showinfo("Program info", "Here u must enter your old password because of security principes!", master=self)
        old_password_tip = Button(self, command=show_tip_for_old_password, text="?",background="#1882FF", foreground="#F0FFF0",  font="Arial 13")
        old_password_tip.place(x=450, y=130)

        new_password_label1 = Label(self, text="New password * :", fg="#1C1C1C", font="Arial 11")
        
        new_password_label1.place(x=20, y=200)
        self.new_password_entry1 = Entry(self, width=30, font='Arial 13',show="●")
        self.new_password_entry1.place(x=180, y=200, width=250)
        def show_tip_for_new_password1():
            messagebox.showinfo("Program info", "Here u must enter your new password! Be carefull and create strong pass!", master=self)
        new_password_tip1 = Button(self, command=show_tip_for_new_password1,text="?",background="#1882FF", foreground="#F0FFF0",  font="Arial 13")
        new_password_tip1.place(x=450, y=200)

        new_password_label2 = Label(self, text="Repeat password * :", fg="#1C1C1C", font="Arial 11")
        new_password_label2.place(x=20, y=260)
        self.new_password_entry2 = Entry(self, width=30, font='Arial 13', show="●")
        self.new_password_entry2.place(x=180, y=260, width=250)
        def show_tip_for_new_password2():
            messagebox.showinfo("Program info", "Here u must reenter your new password one more time! Be carefull!", master=self)
        new_password_tip2 = Button(self, command=show_tip_for_new_password2, text="?",background="#1882FF", foreground="#F0FFF0",  font="Arial 13")
        new_password_tip2.place(x=450, y=260)

        password_tip_entry = Label(self, text="Please be carefful when u change your password!", fg="#1C1C1C", font="Arial 11")
        password_tip_entry.place(x=100, y=330)

        change_pass_button=Button(self, command=self.get_passwords_from_inputs, text="Change Password",background="#1882FF", foreground="#F0FFF0", padx="20", pady="8",  font="Arial 13")  
        change_pass_button.place(x=170, y=370)

        separator2 = Separator(self, orient='horizontal')
        separator2.place(width=460, x=20, y=450)

        close_programm_button=Button(self, command=self.close_window, text="Close and exit",background="#3B6D6D", foreground="#F0FFF0", padx="20", pady="8",  font="Arial 13")  
        close_programm_button.place(x=185, y=470) 

    def __init__(self, usrnm):
        super().__init__()
        self.__username = usrnm
        self.title('Personal page')
        self.geometry('500x600')
        self.resizable(False,False)
        self._old_password_text, self._new_password1,  self._new_password2  = StringVar(), StringVar(), StringVar()
        self.create_widgets()

 
class Admin_Profile(User_Profile):

    def create_table_of_users(self):
        columns = ('usrnm', 'is_locked', 'limitation')
        self.scrollbar_table = Treeview(self, columns=columns, show='headings')
        self.scrollbar_table.heading('usrnm', text='Username')
        self.scrollbar_table.heading('is_locked', text='Locked')
        self.scrollbar_table.heading('limitation', text='Limitation of password')

        data = read_data_from_database(db_name)
        for i in data:
            self.scrollbar_table.insert("", END, values=(str(i["username"]), str(i["is_locked"]), str(i["password_limit"])) )
        
        scrollbar = Scrollbar(self, orient=VERTICAL, command=self.scrollbar_table.yview)
        self.scrollbar_table.configure(yscroll=scrollbar.set)

        #scrollbar.place(x=1150, y=50, height=230)
        self.scrollbar_table.place(x=550,y=50)

    def add_new_user(self):
        name = askstring('System', 'Enter username of new user!', parent=self)
        if name:
            list_of_users = read_data_from_database(db_name)
            for i in list_of_users:
                if i["username"]==name:
                    # if user with this username exist...
                    messagebox.showinfo("System", "There is user with this name! Please Choose another one!", master=self)
                    return
            new_user_data =  {
                "username":name,
                "password":"d41d8cd98f00b204e9800998ecf8427e",
                "is_locked": 0,
                "password_limit":0,
            }
            list_of_users.append(new_user_data)

            # Rewrite file...
            write_data_to_database(db_name, list_of_users)
            self.scrollbar_table.insert("", END, values=(new_user_data["username"], new_user_data["is_locked"], new_user_data["password_limit"]) )
            messagebox.showinfo('System!', "User " + name + " was added succesfuly!", master=self)

    def set_or_unset_limitation_on_user(self, block_or_limit):
        temp_variable_to_change  = "is_locked"  if block_or_limit == "block"  else  "password_limit"
        for selected_item in self.scrollbar_table.selection():
            record = self.scrollbar_table.item(selected_item)["values"]
            if record[0]!="admin":
                if messagebox.askyesno("Program info", "Are u sure u want to change " + block_or_limit + " state of " + str(record[0]) + " user?", icon ='warning', master=self):
                    user_data = read_data_from_database(db_name)
                    for user_record in user_data:
                        if user_record["username"]==str(record[0]):
                            if user_record[temp_variable_to_change]:
                                # if var == 1 -> set 0
                                user_record[temp_variable_to_change] = 0
                                block_or_limit = "un" + block_or_limit
                            else:
                                # if var == 0 -> set 1
                                user_record[temp_variable_to_change] = 1
                            self.scrollbar_table.item(self.scrollbar_table.selection()[0], values=(user_record["username"], user_record["is_locked"], user_record["password_limit"]))
                            messagebox.showinfo("Program info", "Successfully " + block_or_limit + "ed!", master=self)
                            write_data_to_database(db_name, user_data)
                else:
                    break
            else:
                messagebox.showinfo("Program info", "U cannot " + block_or_limit + " admin user!!!", icon="error", master=self)

    def create_admin_widgets(self):
        super().create_widgets()
        separator = Separator(self, orient='vertical')
        separator.place(height=520, x=500, y=40)
        admin_greeting = "This is your admin panel!"
        admin_greeting_label = Label(self, text=admin_greeting, fg="#1C1C1C", font="Arial 14")
        admin_greeting_label.place(x=750, y=5)

        add_user_button = Button(self, command=self.add_new_user, text="Add new user",background="#1882FF", foreground="#F0FFF0",  font="Arial 13")
        add_user_button.place(x=550, y=300)

        block_user_button = Button(self, command=lambda: self.set_or_unset_limitation_on_user("block"), text="Block/unblock user",background="#1882FF", foreground="#F0FFF0",  font="Arial 13")
        block_user_button.place(x=720, y=300)

        limit_user_button = Button(self, command=lambda: self.set_or_unset_limitation_on_user("limit"), text="Limit/unlimit user password",background="#1882FF", foreground="#F0FFF0",  font="Arial 13")
        limit_user_button.place(x=950, y=300)

        # unblock_user_button = Button(self,  command=lambda: self.set_or_unset_limitation_on_user("unblock"), text="Unblock user",background="#1882FF", foreground="#F0FFF0",  font="Arial 13")
        # unblock_user_button.place(x=700, y=500)

        # unlimit_user_button = Button(self,  command=lambda: self.set_or_unset_limitation_on_user("unlimit"), text="Unlimit user password",background="#1882FF", foreground="#F0FFF0",  font="Arial 13")
        # unlimit_user_button.place(x=900, y=500)

        self.create_table_of_users()

    def __init__(self, usrnm):
        super().__init__(usrnm)
        self.geometry('1200x600')
        self.create_admin_widgets()


class Login_window(Tk):
    __counter_of_invalid_username = 0
    __counter_of_invalid_passwords = 0

    def create_login_widgets(self):
        greeting = "Hello dear user!\nThis is password authentication programm!"
        greeting_label = Label(self, text=greeting,background="#00FF00", fg="#1C1C1C", font="Arial 14")
        greeting_label.grid(row=0, columnspan=2)

        #----- User field -----
        username_label = Label(self, text="Username: ", fg="#1C1C1C", font="Arial 15")
        username_label.grid(row=1, column=0, sticky=E, padx=20, pady=20)

        username_entry = Entry(self, textvariable=self.__username_text, width=30, font='Arial 13')
        username_entry.grid(row=1, column=1,sticky=W,padx=20, pady=20)

        #----- Pass field -----
        password_label = Label(self, text="Password: ", fg="#1C1C1C", font="Arial 15")
        password_label.grid(row=2, column=0, sticky=E,padx=20, pady=20)

        password_entry = Entry(self, textvariable=self.__password_text, width=30, font='Arial 13', show="●")
        password_entry.grid(row=2, column=1, sticky=W, padx=20, pady=20)

        #----- Login button ------
        login_button=Button(self, command=self.get_password_and_username, text="Login",background="#FF0033", foreground="#F0FFF0", padx="20", pady="8",  font="Arial 13")
        login_button.grid(row=3, columnspan=2)

        #----- Menu ------
        def show_creator_info():
            messagebox.showinfo("Programm info", "This programm was created by Snigur Antor FB-91\nVaraiant №19", master=self)
        def show_info_about_programm():
            messagebox.showinfo("Programm info", "This programm was created for users based on pasword authentication!", master=self)

        menu_info, sub_menu = Menu(self), Menu(tearoff=0)
        sub_menu.add_cascade(label="Author", command=show_creator_info)
        sub_menu.add_cascade(label="About", command=show_info_about_programm)
        menu_info.add_cascade(label="Help",menu=sub_menu)
        self.config(menu=menu_info)

    def __init__(self):
        super().__init__()
        self.__username_text, self.__password_text = StringVar(), StringVar()
        self.title("My_lab")
        self.geometry('700x550')
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.create_login_widgets()
        if not os.path.exists(db_name):
            self.create_user_default_db()

    def close_app(self):
        self.destroy()

    def create_user_default_db(self):
        credentials = [
                {
                    "username": "",
                    "password": "",
                    "is_locked": "",
                    "password_limit":"",
                }
        ]
        admin_deffault_user = "admin"
        admin_deffault_password = ""
        credentials[0]["username"] = admin_deffault_user
        credentials[0]["password"] = (hashlib.md5(admin_deffault_password.encode()).hexdigest())
        credentials[0]["is_locked"] = 0
        credentials[0]["password_limit"] = 0

        # x =  { 
        #         "username":"GeeksForGeeks",
        #         "password":"Noida",
        #         "is_locked": 0,
        #         "password_limit": 0
        # }
        # credentials.append(x)
        #print((credentials))
        write_data_to_database(db_name, credentials)
    
    def log_in_app(self, username, password):
        if os.path.exists(db_name):
            with open(db_name) as f_db:
                list_of_users = json.load(f_db)
            for user in list_of_users:
                if user["username"]==username:
                    if user["password"]!=password:
                        # Wrong pass... 
                        self.__counter_of_invalid_passwords += 1
                        if self.__counter_of_invalid_passwords !=3:
                            messagebox.showwarning("Programm info","Wrong password! Please try again!", master=self)
                        else:
                            messagebox.showerror("Programm info","Too many attempts with incorrect password!", master=self)
                            self.close_app()
                    else:
                        # Logging....
                        if user["is_locked"]:
                            messagebox.showwarning("Programm info","Sorry your account was blocked! Please contact administrator!", master=self)
                        else:
                            if self.__username_text.get() == "admin":
                                profile_window = Admin_Profile(self.__username_text.get())
                            else:
                                profile_window = User_Profile(self.__username_text.get())
                            self.close_app()
                            profile_window.mainloop()
                    return     
            # # Wrong usrnm...
            self.__counter_of_invalid_username +=1
            if self.__counter_of_invalid_username == 2:
                messagebox.showerror("Programm info","Too many attempts with invalid usernames!", master=self)
                self.close_app()
            else:
                messagebox.showwarning("Programm info","There is no user! Please try again! U have one more chance!", master=self)
        else:
            messagebox.showerror("Programm info","Problem with database!", master=self)

    def get_password_and_username(self):
        if self.__username_text.get() == "":
            messagebox.showwarning("Programm info","Please enter username!", master=self)
        else:
            self.log_in_app(self.__username_text.get(), hashlib.md5(self.__password_text.get().encode()).hexdigest())


if __name__ == "__main__":
    req_window = Login_window()
    req_window.mainloop()