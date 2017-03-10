##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##                          This program was written by Shady Salaheldin
##                                  shady.a.salaheldin@gmail.com
##                                 GUI_FOR_PDF_GRABBER_v0_0_1_3.py
##                      ~~!!! TO BE USED WITH : PDF_GRABBER_v0_0_1_3.py !!!~~
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################

import tkinter
import PDF_GRABBER_v0_0_1_3 as GRABBER
import threading
import os

top = tkinter.Tk()
top.title("PDF_GRABBER")
def submit(E1_Query_Field,List_box):
    List_box.delete(0,tkinter.END)
    pdf_list = GRABBER.DO_QUERY_FOR_GUI(E1_Query_Field.get())
    creat_list_box(pdf_list,List_box)
def creat_list_box(pdf_list,List_box):    
    counter = 1
    for x in pdf_list:
        List_box.insert(counter,str(x))
        counter = counter+1
def download_all(List_box,FOLDER):
    pdf_list= List_box.get (0,tkinter.END)
    if not os.path.exists(FOLDER):
            os.makedirs(FOLDER)
    for x in pdf_list:
        threading.Thread(target=GRABBER.download_pdf_from_link,args=(x,FOLDER)).start()
def download_selection(List_box,FOLDER):
    pdf_list_index= List_box.curselection()
    pdf_list = []
    for x in pdf_list_index:
        pdf_list.append(List_box.get(x))
    if not os.path.exists(FOLDER):
            os.makedirs(FOLDER)
    for x in pdf_list:
        if x != None:
            threading.Thread(target=GRABBER.download_pdf_from_link,args=(x,FOLDER)).start()
##    for x in pdf_list:
##        threading.Thread(target=GRABBER.download_pdf_from_link,args=(x,FOLDER)).start()

top.resizable(width=False, height=False)
top.geometry('{}x{}'.format(1280, 920))



L1 = tkinter.Label(top, text="User Query: ")
L1.pack(side = tkinter.TOP)
E1 = tkinter.Entry(top, bd =5,width=100)
E1.pack(side = tkinter.TOP)
B1 = tkinter.Button(top, text ="Submit!", command= lambda: submit(E1,Lb1))
B1.pack(side = tkinter.TOP)
Lb1 = tkinter.Listbox(top,height=40, width = 150,selectmode=tkinter.MULTIPLE,selectbackground='yellow')
Lb1.pack(side = tkinter.TOP)
B2 = tkinter.Button(top, text ="Download Selection!", command= lambda: download_selection(Lb1,E1.get()))
B2.pack(side = tkinter.TOP)
B3 = tkinter.Button(top, text ="Download ALL!", command= lambda: download_all(Lb1,E1.get()))
B3.pack(side = tkinter.TOP)

# Code to add widgets will go here...
top.mainloop()
