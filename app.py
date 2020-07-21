try:
    import tkinter as tk    
    from tkinter import *
    from tkinter import messagebox as mb
except ImportError:
    import Tkinter as tk
    from Tkinter import *
    from Tkinter import messagebox as mb
from db import Database
import clipboard as cbl
db = Database('swiftpass.db')

class Application(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        self.entrys = []
        self.textboxes = []
        self.asterisks = 1
        self.selected_index = 0 
        self.previous_index = None
        self.update_flag = False
        self.action_flag = 0 
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        parent.title('SwiftPass')
        parent.geometry('700x700')
        parent.bind('<ButtonPress-1>', self.deselect_lb_item)

        #parent.bind("<<FocusIn>>", self.onfocus)
        self.generate_widgets()
        self.populate_data()
    def generate_widgets(self):
        self.serviceid_text = StringVar()
        self.serviceid_label = Label(self.parent, text='Service ID', font=('bold', 14,), pady=20, padx=5)
        self.serviceid_label.grid(row=0, column=0,sticky=W)
        self.serviceid_entry = Entry(self.parent, textvariable=self.serviceid_text)
        self.serviceid_entry.grid(row=0, column=1)
        self.entrys.append(self.serviceid_entry)
        self.textboxes.append(self.serviceid_text)

        self.service_text = StringVar()
        self.service_label = Label(self.parent, text='Service Name', font=('bold', 14), pady=20, padx=5)
        self.service_label.grid(row=1, column=0,sticky=W)
        self.service_entry = Entry(self.parent, textvariable=self.service_text)
        self.service_entry.grid(row=1, column=1)
        self.entrys.append(self.service_entry)
        self.textboxes.append(self.service_text)


        self.url_text = StringVar()
        self.url_label = Label(self.parent, text='URL', font=('bold', 14), pady=20, padx=5)
        self.url_label.grid(row=2, column=0, sticky=W)
        self.url_entry = Entry(self.parent, textvariable=self.url_text)
        self.url_entry.grid(row=2, column =1)
        self.entrys.append(self.url_entry)
        self.textboxes.append(self.url_text)


        self.username_text = StringVar()
        self.username_label = Label(self.parent, text='Username', font=('bold,', 14), pady=20, padx=5)
        self.username_label.grid(row=3, column=0, stick=W)
        self.username_entry = Entry(self.parent, textvariable=self.username_text)
        self.username_entry.grid(row=3, column=1)
        self.entrys.append(self.username_entry)
        self.textboxes.append(self.username_text)



        self.password_text=StringVar()
        self.password_label = Label(self.parent, text='Password', font =('bold',14), pady=20, padx=5)
        self.password_label.grid(row=4, column=0, sticky=W)
        self.password_entry = Entry(self.parent, textvariable=self.password_text)
        self.password_entry.grid(row=4, column=1)
        self.entrys.append(self.password_entry)
        self.textboxes.append(self.password_text)



        self.password_list = Listbox(self.parent, height=20, width=50, border=1)
        self.password_list.grid(row=5, column=0, padx=5, columnspan=3, rowspan=6)
        self.password_list.bind('<<ListboxSelect>>', self.select)
        #self.scrollbar = tk.Scrollbar(self.parent)
        #self.scrollbar.grid(row=3, column=2)

        #self.password_list.config(yscrollcommand=self.scrollbar.set)
        #self.scrollbar.config(command=self.password_list.yview)

        self.add_btn = Button(self.parent, text='Add Service', width=12, command=self.add_service)
        self.add_btn.grid(row=0, column=3, pady=20,padx=5)

        self.remove_btn = Button(self.parent, text='Remove Service', width=12, command=self.remove_service)
        self.remove_btn.grid(row=0, column=4, pady=20, padx=5)

        self.edit_btn = Button(self.parent, text='Edit Service', width=12,command=self.edit_service)
        self.edit_btn.grid(row=1, column=3, pady=20, padx=5)

        self.show_passwords_btn = Button(self.parent, text='Show Passwords', width=12, command=self.toggle_show_passwords)
        self.show_passwords_btn.grid(row=1, column=4, pady=20, padx=5)

        self.save_btn = Button(self.parent, text='Save', width=12, command=self.save,state='disabled')
        self.save_btn.grid(row=2, column=3, pady=20, padx=5)

        self.cancel_btn = Button(self.parent, text='Cancel', width=12, command=self.cancel,state='disabled')
        self.cancel_btn.grid(row=2, column=4, pady=20, padx=5)

        self.copy_url_btn = Button(self.parent, text='Copy', width=12, command= lambda : self.clipboard(self.url_entry.get()))
        self.copy_url_btn.grid(row =2, column=2)

        self.copy_uname_btn = Button(self.parent, text='Copy', width=12, command= lambda : self.clipboard(self.username_entry.get()))
        self.copy_uname_btn.grid(row =3, column=2)    

        self.copy_pass_btn = Button(self.parent, text='Copy', width=12, command= lambda : self.clipboard(db.get_password(self.serviceid_entry.get())))
        self.copy_pass_btn.grid(row =4, column=2) 
       # self.toggle_tb(1)

    def deselect_lb_item(self, event):
        if self.selected_index == self.previous_index:
            self.password_list.selection_clear(0, tk.END)
        self.previous_index = self.password_list.curselection()

    def populate_data(self):
        self.password_list.delete(0, END)

        if self.asterisks == 1:
            for row in db.fetch():
                self.anonyimise_listbox(row)
        if self.asterisks == 0:
            for row in db.fetch():
                self.password_list.insert(END, row)
        self.password_list.select_set(self.selected_index)
        self.password_list.event_generate("<<ListboxSelect>>")
    
    def anonyimise_listbox(self, data):
        pwd = self.anonymise(str(data[4]))
        data_list = list(data)
        data_list[4]=pwd
        new_row = tuple(data_list)
        self.password_list.insert(END, new_row)
    def unan_listbox(self):
        self.populate_data()

    def toggle_show_passwords(self):
        changed_flag = False
        if self.asterisks ==1: 
            self.asterisks = 0
            self.populate_data()
            changed_flag = True
        if self.asterisks == 0 and changed_flag is False:
            self.asterisks = 1
            self.password_list.delete(0, END)

            
            for row in db.fetch():
                self.anonyimise_listbox(row)
        self.password_list.select_set(self.selected_index)
        self.password_list.event_generate("<<ListboxSelect>>")
    
    def anonymise(self, password):
        return "*"*len(password)
    def add_service(self):
        self.clear()
        self.toggle_tb(0)
        self.action_flag='add'
        self.add_btn["state"] = "disabled"
        self.remove_btn["state"] = "disabled"
        self.edit_btn["state"] = "disabled"
        self.show_passwords_btn["state"] = "disabled"
        self.password_list["state"] = "disabled"
        self.save_btn["state"] = "active"
        self.cancel_btn["state"] = "active"       
    def cancel(self):
        self.toggle_tb(1)
        self.save_btn["state"] = "disabled"
        self.cancel_btn["state"] = "disabled"   
        self.add_btn["state"] = "active"
        self.remove_btn["state"] = "active"
        self.edit_btn["state"] = "active"
        self.password_list["state"] = "normal"
        self.show_passwords_btn["state"] = "active"               
        return

    def save(self):
        allow = False
        if self.action_flag == 'add':
            if self.insert_service() !=-1:
                allow = True

        if self.action_flag == 'edit':
            if self.commit_edit() !=-1:
                allow = True
        if allow is True:
            self.toggle_tb(1)
            self.save_btn["state"] = "disabled"
            self.cancel_btn["state"] = "disabled"  
            self.add_btn["state"] = "active"
            self.remove_btn["state"] = "active"
            self.edit_btn["state"] = "active"
            self.show_passwords_btn["state"] = "active"    
            self.password_list["state"] = "normal"
            self.populate_data()
    def insert_service(self):
        if self.check() == -1: return -1
        db.insert(self.service_entry.get(), self.url_entry.get(), str(self.username_entry.get()), self.password_entry.get())
        self.populate_data()


    def check(self):
        if len(self.service_entry.get()) == 0 or len(self.username_entry.get()) == 0 or len(self.url_entry.get()) == 0 or len(self.password_entry.get()) == 0:
            mb.showerror("Error", "Please ensure all fields contain data")
            return -1
        return 1

    def edit_service(self):

        self.toggle_tb(0)
        self.add_btn["state"] = "disabled"
        self.remove_btn["state"] = "disabled"
        self.edit_btn["state"] = "disabled"
        self.show_passwords_btn["state"] = "disabled"
        self.password_list["state"] = "disabled"
        self.save_btn["state"] = "active"
        self.cancel_btn["state"] = "active"  
        self.action_flag='edit'
    
    def commit_edit(self):
        if self.check()==-1: return
        db.update(self.serviceid_entry.get(), self.service_entry.get(), self.url_entry.get(), str(self.username_entry.get()), self.password_entry.get())
        self.populate_data()

    def remove_service(self):
        return
    def clear(self):
        for tb in self.textboxes:
            tb.set('')
        return

    def toggle_tb(self, flag):
        if flag == 1:
            for tb in self.entrys:
                tb.config(state='disabled')
            return
        for tb in self.entrys:
            tb.config(state='normal')
        self.serviceid_entry.config(state='disabled')
    def select(self, event):
        sel= self.password_list.get(self.password_list.curselection())
        self.selected_index = self.password_list.curselection()
        service_id = sel[0]
        service_name = sel[1]
        url = sel[2]
        username = sel[3]
        password = sel[4]
        self.serviceid_text.set(service_id)
        self.service_text.set(service_name)
        self.url_text.set(url)
        self.username_text.set(username)
        if self.asterisks == 1:
            password = self.anonymise(password)
        self.password_text.set(password)
        print(sel)
    def clipboard(self, arg):
        cbl.copy(arg)



    #def comb_funcs(*funcs):
     #       for func in funcs:
    ##    def comb_func(*arguments, **kwarguments):
    #    return comb_func
    #            func(*arguments, **kwarguments)
   



root = tk.Tk()
Application(root). mainloop()
del db
