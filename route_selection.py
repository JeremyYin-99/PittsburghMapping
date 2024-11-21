# This is the gui route selection
from tkinter import *
from tkinter.constants import BROWSE, MULTIPLE
import webbrowser
import os

def route_select_t1(route_names): 

    root = Tk()
    root.geometry('500x300')

    prompt = Label(root, text='Select a route below')

    ls = StringVar(value=route_names)
    route_lb = Listbox(root,listvariable=ls, selectmode='browse')

    def route_get():
        cwd = os.getcwd()
        for i in route_lb.curselection():
            filename = 'file://'+str(cwd)+'/Maps/'+str(route_lb.get(i))+'.html'
            webbrowser.open(filename)
            print(route_lb.get(i))



    run_button = Button(root, text='click after selecting', command=route_get)


    prompt.pack()
    route_lb.pack()
    run_button.pack()

    root.mainloop()
