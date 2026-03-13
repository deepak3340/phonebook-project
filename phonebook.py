from tkinter import *
from tkinter import ttk
import mysql.connector as ct

def connect_db():
    return ct.connect(
        host="localhost",
        user="root",
        password="deepak",
        database="phonebook"
    )

def add_contact():
    name=ename.get()
    phone=ephone.get()

    conn=connect_db()
    cur=conn.cursor()

    cur.execute("insert into contacts(name,contact) values(%s,%s)",(name,phone))
    conn.commit()
    conn.close()

    show_all()
    
def show_all():
    conn=connect_db()
    cur=conn.cursor()

    cur.execute("select name,contact from contacts")
    rows=cur.fetchall()

    for i in t.get_children():
        t.delete(i)

    for r in rows:
        t.insert("",END,values=r)

    conn.close()

def search(event):
    name=ename.get()

    conn=connect_db()
    cur=conn.cursor()

    cur.execute("select name,contact from contacts where name like %s",(name+"%",))
    rows=cur.fetchall()

    for i in t.get_children():
        t.delete(i)

    for r in rows:
        t.insert("",END,values=r)

    conn.close()

def delete_contact():
    selected=t.selection()

    if selected:
        values=t.item(selected)['values']
        name=values[0]

        conn=connect_db()
        cur=conn.cursor()

        cur.execute("delete from contacts where name=%s",(name,))
        conn.commit()
        conn.close()

        show_all()


def clear():
    ename.delete(0,END)
    ephone.delete(0,END)

win=Tk()
win.title("Phonebook Manager")
win.geometry("600x500")
win.configure(bg="#f0f2f5")

title=Label(win,text=" Phonebook Manager",
font=("Segoe UI",20,"bold"),
bg="#f0f2f5",
fg="#2c3e50")

title.pack(pady=15)

frame=Frame(win,bg="#f0f2f5")
frame.pack(pady=10)

Label(frame,text="Name",
font=("Segoe UI",12),
bg="#f0f2f5").grid(row=0,column=0,padx=10,pady=8)

Label(frame,text="Phone",
font=("Segoe UI",12),
bg="#f0f2f5").grid(row=1,column=0,padx=10,pady=8)

ename=Entry(frame,font=("Segoe UI",12),width=25)
ename.grid(row=0,column=1)

ephone=Entry(frame,font=("Segoe UI",12),width=25)
ephone.grid(row=1,column=1)

ename.bind("<KeyRelease>",search)

btnframe=Frame(win,bg="#f0f2f5")
btnframe.pack(pady=15)

Button(btnframe,text="Add",
width=10,bg="#27ae60",fg="white",
font=("Segoe UI",10,"bold"),
command=add_contact).grid(row=0,column=0,padx=6)

Button(btnframe,text="Delete",
width=10,bg="#e74c3c",fg="white",
font=("Segoe UI",10,"bold"),
command=delete_contact).grid(row=0,column=1,padx=6)

Button(btnframe,text="Clear",
width=10,bg="#f39c12",fg="white",
font=("Segoe UI",10,"bold"),
command=clear).grid(row=0,column=2,padx=6)

Button(btnframe,text="Show All",
width=10,bg="#3498db",fg="white",
font=("Segoe UI",10,"bold"),
command=show_all).grid(row=0,column=3,padx=6)

style=ttk.Style()
style.theme_use("default")

style.configure("Treeview",
font=("Segoe UI",11),
rowheight=28)

style.configure("Treeview.Heading",
font=("Segoe UI",12,"bold"))

table_frame=Frame(win)
table_frame.pack(pady=10,fill=BOTH,expand=True)

scroll=Scrollbar(table_frame)
scroll.pack(side=RIGHT,fill=Y)

t=ttk.Treeview(table_frame,
columns=("name","contact"),
show="headings",
yscrollcommand=scroll.set)

t.heading("name",text="Name")
t.heading("contact",text="Contact")

t.column("name",width=200)
t.column("contact",width=200)

t.pack(fill=BOTH,expand=True)

scroll.config(command=t.yview)

show_all()

win.mainloop()