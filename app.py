#python2/3 compatability
try:
    import tkinter as tk    
    from tkinter import StringVar, Label, N, E, S, W, Entry, Listbox, Button, END
    from tkinter import messagebox as mb
except ImportError:
    import Tkinter as tk
    from Tkinter import StringVar, Label, N, E, S, W, Entry, Listbox, Button, END
    from Tkinter import messagebox as mb
import clipboard as cbl
from db import PasswordDatabase
import random
import string
#create database and connection
db = PasswordDatabase('swiftpass.db')
key =''

class User:
    def _init__(self, name, master_password):
        self.name = name
        self.master_password = master_password
        self.key = ''




#Tkinter class
class Application(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        self.entrys = []
        self.textboxes = []
        self.asterisks = 1
        self.selected_index = 0 
        self.previous_index = None
        self.update_flag = False
        self.action_flag = 0 
        self.previous_key = ''
        self.new_key = ''
        #init frame
        print('INITIALISING FRAME')
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        #Set window name, size
        parent.title('SwiftPass')
        parent.geometry('700x700')
        #on mouse1 click, deselect listbox
        parent.bind('<ButtonPress-1>', self.deselect_lb_item)
        self.generate_widgets()
        self.populate_data()
    def generate_widgets(self):
        print('GENERATING WIDGETS')

        #Service ID
        self.serviceid_text = StringVar()
        self.serviceid_label = Label(self.parent, text='Service ID', font=('bold', 14,), pady=20, padx=5)
        self.serviceid_label.grid(row=0, column=0,sticky=W)
        self.serviceid_entry = Entry(self.parent, textvariable=self.serviceid_text)
        self.serviceid_entry.grid(row=0, column=1)
        self.entrys.append(self.serviceid_entry)
        self.textboxes.append(self.serviceid_text)

        #Service Name
        self.service_text = StringVar()
        self.service_label = Label(self.parent, text='Service Name', font=('bold', 14), pady=20, padx=5)
        self.service_label.grid(row=1, column=0,sticky=W)
        self.service_entry = Entry(self.parent, textvariable=self.service_text)
        self.service_entry.grid(row=1, column=1)
        self.entrys.append(self.service_entry)
        self.textboxes.append(self.service_text)

        #URL
        self.url_text = StringVar()
        self.url_label = Label(self.parent, text='URL', font=('bold', 14), pady=20, padx=5)
        self.url_label.grid(row=2, column=0, sticky=W)
        self.url_entry = Entry(self.parent, textvariable=self.url_text)
        self.url_entry.grid(row=2, column =1)
        self.entrys.append(self.url_entry)
        self.textboxes.append(self.url_text)

        #Username
        self.username_text = StringVar()
        self.username_label = Label(self.parent, text='Username', font=('bold,', 14), pady=20, padx=5)
        self.username_label.grid(row=3, column=0, stick=W)
        self.username_entry = Entry(self.parent, textvariable=self.username_text)
        self.username_entry.grid(row=3, column=1)
        self.entrys.append(self.username_entry)
        self.textboxes.append(self.username_text)


        #Password
        self.password_text=StringVar()
        self.password_label = Label(self.parent, text='Password', font =('bold',14), pady=20, padx=5)
        self.password_label.grid(row=4, column=0, sticky=W)
        self.password_entry = Entry(self.parent, textvariable=self.password_text)
        self.password_entry.grid(row=4, column=1)
        self.entrys.append(self.password_entry)
        self.textboxes.append(self.password_text)


        #Listbox
        self.password_list = Listbox(self.parent, height=20, width=50, border=1)
        self.password_list.grid(row=5, column=0, padx=5, columnspan=3, rowspan=6)
        self.password_list.bind('<<ListboxSelect>>', self.select)
        #self.scrollbar = tk.Scrollbar(self.parent)
        #self.scrollbar.grid(row=3, column=2)

        #self.password_list.config(yscrollcommand=self.scrollbar.set)
        #self.scrollbar.config(command=self.password_list.yview)

        #Add button
        self.add_btn = Button(self.parent, text='Add Service', width=12, command=self.add_service,fg='black',foreground='black',highlightbackground='black')
        self.add_btn.grid(row=0, column=3, pady=20,padx=5)

        #Remove button
        self.remove_btn = Button(self.parent, text='Remove Service', width=12, command=self.remove_service,fg='black',foreground='black',highlightbackground='black')
        self.remove_btn.grid(row=0, column=4, pady=20, padx=5)

        #Edit button
        self.edit_btn = Button(self.parent, text='Edit Service', width=12,command=self.edit_service,fg='black',foreground='black',highlightbackground='black')
        self.edit_btn.grid(row=1, column=3, pady=20, padx=5)

        #Show Password button
        self.show_passwords_btn = Button(self.parent, text='Show Passwords', width=12, command=self.toggle_show_passwords,fg='black',foreground='black',highlightbackground='black')
        self.show_passwords_btn.grid(row=1, column=4, pady=20, padx=5)

        #Save button
        self.save_btn = Button(self.parent, text='Save', width=12, command=self.save,state='disabled',fg='black', foreground='black',highlightbackground='black')
        self.save_btn.grid(row=2, column=3, pady=20, padx=5)

        #Cancel button
        self.cancel_btn = Button(self.parent, text='Cancel', width=12, command=self.cancel,state='disabled',fg='black',foreground='black',highlightbackground='black')
        self.cancel_btn.grid(row=2, column=4, pady=20, padx=5)

        #Copy URL button
        self.copy_url_btn = Button(self.parent, text='Copy', width=12, command= lambda : self.clipboard(self.url_entry.get()),fg='black',foreground='black',highlightbackground='black')
        self.copy_url_btn.grid(row =2, column=2)

        #Copy Username button
        self.copy_uname_btn = Button(self.parent, text='Copy', width=12, command= lambda : self.clipboard(self.username_entry.get()),fg='black',foreground='black',highlightbackground='black')
        self.copy_uname_btn.grid(row =3, column=2)    

        #Copy Password button
        self.copy_pass_btn = Button(self.parent, text='Copy', width=12, command= lambda : self.clipboard(db.get_password(self.serviceid_entry.get())),fg='black',foreground='black',highlightbackground='black')
        self.copy_pass_btn.grid(row =4, column=2) 
        #self.toggle_tb(1)

        self.generate_secure_password_32_btn = Button(self.parent, text='Generate (32)', width=12,fg='black',foreground='black',highlightbackground='black', command = lambda: self.password_text.set(self.generate_password(32)))
        self.generate_secure_password_32_btn.grid(row=4, column=3)

        self.generate_secure_password_64_btn = Button(self.parent, text='Generate (64)', width=12,fg='black',foreground='black',highlightbackground='black', command = lambda: self.password_text.set(self.generate_password(64)))
        self.generate_secure_password_64_btn.grid(row=4, column=4)        

    #Deselect currently selected listbox item
    def deselect_lb_item(self, event):
        print('DESELECTED LISTBOX')
        if self.selected_index == self.previous_index:
            self.password_list.selection_clear(0, tk.END)
        self.previous_index = self.password_list.curselection()

    def populate_data(self):
        #clear listbox
        print('POPULATING DATA')
        self.password_list.delete(0, END)

        if self.asterisks == 1:
            for row in db.fetch():
                #anonyimise password
                self.anonyimise_listbox(row)
        if self.asterisks == 0:
            for row in db.fetch():
                #insert row to listbox
                self.password_list.insert(END, row)

        self.password_list.select_set(self.selected_index)
        self.password_list.event_generate("<<ListboxSelect>>")
    
    def anonyimise_listbox(self, data):
        print('ANONYIMISING DATA')
        #anonyimise password
        pwd = self.anonymise(str(data[4]))
        data_list = list(data)
        data_list[4]=pwd
        new_row = tuple(data_list)
        #insert password
        self.password_list.insert(END, new_row)
    def unan_listbox(self):
        print('UNANYMISING DATA')
        #reinit data
        self.populate_data()

    def toggle_show_passwords(self):
        print('TOGGLING SHOW PASSWORDS')
        changed_flag = False
        if self.asterisks ==1: 
            self.asterisks = 0
            #reinit data
            self.populate_data()
            changed_flag = True
        if self.asterisks == 0 and changed_flag is False:
            self.asterisks = 1
            #clear listbox
            self.password_list.delete(0, END)
            
            for row in db.fetch():
                #anonymise password
                self.anonyimise_listbox(row)
        self.password_list.select_set(self.selected_index)
        self.password_list.event_generate("<<ListboxSelect>>")
    
    def anonymise(self, password):
        #return anonyimised password
        return "*"*len(password)
    def add_service(self):
        print('BEGIN ADD SERVICE')
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
        print('CANCEL ACTION')
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
        print('SAVING ACTION')
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
        print('ATTEMPTING INSERT TO DATABASE')
        if self.check() == -1: return-1
        #insert data to be database
        print('INSERT SUCCESSFUL')
        db.insert(self.service_entry.get(), self.url_entry.get(), str(self.username_entry.get()), self.password_entry.get())
        self.populate_data()


    def check(self):
        #length check
        if len(self.service_entry.get()) == 0 or len(self.username_entry.get()) == 0 or len(self.url_entry.get()) == 0 or len(self.password_entry.get()) == 0:
            #show message box
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
        #update database
        db.update(self.serviceid_entry.get(), self.service_entry.get(), self.url_entry.get(), str(self.username_entry.get()), self.password_entry.get())
        self.populate_data()

    def remove_service(self):
        id = self.serviceid_entry.get()
        db.remove(id)
        self.populate_data()
    def clear(self):
        #clear textboxes
        for tb in self.textboxes:
            tb.set('')
        return

    def toggle_tb(self, flag):
        #enable/disable textboxes
        if flag == 1:
            for tb in self.entrys:
                tb.config(state='disabled')
            return
        for tb in self.entrys:
            tb.config(state='normal')
        self.serviceid_entry.config(state='disabled')
    def select(self, event):
        #insert selected listbox item into textboxes
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
        #check if we need to anonymise
        if self.asterisks == 1:
            password = self.anonymise(password)
        self.password_text.set(password)
    def clipboard(self, arg):
        #copy to clipboard
        cbl.copy(arg)

    def generate_password(self, len):
        return ''.join(random.choice(string.ascii_letters) for i in range(len))


#init, run app
root = tk.Tk()
Application(root). mainloop()
#cleanup
del db
