##                          This program was written by Shady Salaheldin
##                                  shady.a.salaheldin@gmail.com
##                                          v0.0.1.4
##                                ~~!!! STAND ALONE GUI !!!~~
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##
##  This program searches the web using duckduckgo.com's html version of the site at:
##                          https://www.duckduckgo.com/html
##  and retrieves and stores all search results that end in .pdf which match the user's query.
##
##  The program them displays all of the links it has retrieved and asks the user
##  if they want to download all of the content or not
##
##  if the user selects yes, the program creates a folder named after the query entered by the user,
##  if it does not already exist.
##  The program then downloads and stores all pdf files in that new folder with the title of the pdf file
##  being same as original pdf file found on web.
##
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##                                          3/7/2017
##                                 Changes added to v0.0.1.1
##          - Created Multithreading for downloading multiple pdfs at same time
##          - The program now checks for file name existing in directory before creating it
##                  if the file exists it enumerates (#) addition to file until it finds one
##                  that does not exist. such as: test, test(2), test(3),......test(#)
##
##
##
##
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##                                          3/8/2017
##                                 Changes added to v0.0.1.2
##          - Added modularity
##          - Added try / except statment for dom tree creation, was previously crashing program
##                  if for example something was mis-spelled and duckduckgo.com/html suggested
##                  changes to spelling.
##          - Added file option where you can pre-set queries within a file.
##            one line per query and the script takes away the last character which is a "\n" (newline)
##          - Attempted to adde File creation DND.txt "Did Not Download"  and DL.txt with links that could
##              not be downloaded and ones that were downloaded for each query, but it is still not
##              functional. Must find a way to write files after all threads are complete.
##
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##                                          3/10/2017
##                                 Changes added to v0.0.1.3
##          - CREATED GUI_FOR_PDF_GRABBER_v0_0_1_3.py
##          - Cloned DO_QUERY into  DO_QUERY_FOR_GUI and modified it to return list of pdf files
##               This Function is used by gui to  get the pdf links list and the GUI will then
##               call the needed threads of download_pdf_from_link function
##          - The GUI now allows for 2 modes after the user enters the query : either download all or
##            Download selection.
##         !- The GUI does not support file query read as in v0.0.1.2
##
##
##                                         UPCOMING CHANGES
##          - Will allow file read for GUI
##          - WIll add Scrolling for List BOX of links incase of increased number of returned links
##          - Will allow for bigger query size, currently set at 150 characters.
##          - CODE CLEANUP AND ADDITIONAL COMMENTING
##
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##                                          3/11/2017
##                                 Changes added to v0.0.1.4
##          - Fixed minor bugs in code in regards to empty lists being iterated
##              Program now checks list is not empty before iterating.
##          - Fixed minor bug in regards to empty querys and interaction with buttons. Added try/except
##            statements.
##          - Previously the program was two file. Now The program is one file.
##
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################



import tkinter
import threading
import urllib
import os
import requests
import xml.dom.minidom



##########################################################################################################
##########################################################################################################
##
##              This function handles download of pdf file from link into specified folder
##              The pdf title in folder becomes the last element of the link provided.
##              This function returns True in sucess and False in faliure to write file.
##
##########################################################################################################
##########################################################################################################

def download_pdf_from_link(link,FOLDER):
    try:
        #print(str(link) +"   "+ FOLDER) #testing purposes
        url = link
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}
        response = requests.get(url,headers=headers)
        book_name = url.split('/')[-1]
        PATH = FOLDER+'/'+book_name
        file_copy_increment= 2 ##will be used to enumerate files with same name
        PATH_FINAL = PATH
        while (os.path.isfile(PATH_FINAL)):
            PATH_FINAL = str(PATH) +"("+file_copy_increment+")"
            file_copy_increment = file_copy_increment+1
        with open(PATH_FINAL, 'wb') as f:
            f.write(response.content)
        return True
    except:
        #print(str(link)+" could not be downloaded")
        return False

##########################################################################################################
##########################################################################################################
##
##              This function handles quering www.duckduckgo.com/html for provided query string
##              This fuction returns a list of all links that end in .pdf
##
##########################################################################################################
##########################################################################################################
def DO_QUERY_FOR_GUI(query_string):
    url_endpoint = 'https://www.duckduckgo.com/html'
    user_query = query_string#[:-1]
    mydict = {'q': str("'"+str(user_query)+"'")}
    resp = requests.get(url_endpoint, params=mydict)
    try:
        dom = xml.dom.minidom.parseString(resp.text)
        list_of_links = dom.getElementsByTagName('a')
        #DL_LIST=[]
        #DND_LIST = []
        pdf_list = []

        for x in list_of_links:
            link=x.getAttribute('href')
            link=link.split('=')[-1]
            if str(link)[-4:] == ".pdf" and pdf_list and str(pdf_list[len(pdf_list)-1]) != str(str(urllib.parse.unquote(link))):
                pdf_list.append(str(urllib.parse.unquote(link)))
            elif not pdf_list: pdf_list.append(str(urllib.parse.unquote(link)))### this line seems redundant at the moment but leaving it for now
                                                                               ### to maintain current functionality.

        ###################################################################################################
        pdf_list.pop(0)
        ####### not sure why the list is created with 1 extra blank item in beginning so i am ridding of it.
        ####### will be patched properly soon.

        return pdf_list
                  
    except:
        print(str(user_query))
        print("An error occured - please try again.")



##########################################################################################################
##########################################################################################################
##
##              This function is for the GUI submit button B1 it extracts query from Entry field E1
##              and calls DO_QUERY_FOR_GUI then passes the pdf list and list box Lb1 to create_list_box
##
##########################################################################################################
##########################################################################################################
def submit(E1_Query_Field,List_box):
    List_box.delete(0,tkinter.END)
    pdf_list = DO_QUERY_FOR_GUI(E1_Query_Field.get())
    create_list_box(pdf_list,List_box)


##########################################################################################################
##########################################################################################################
##
##              This function is for the GUI ListBox Lb1 to populate the list box with pdf links from
##              pdf_list
##
##########################################################################################################
##########################################################################################################
def create_list_box(pdf_list,List_box):    
    counter = 1
    for x in pdf_list:
        if x != None:
            List_box.insert(counter,str(x))
            counter = counter+1


##########################################################################################################
##########################################################################################################
##
##              This function is for the GUI download all button B3 it grabs all of the links in ListBox
##              Lb1 and puts them in designated folder correspoding to user's query
##
##########################################################################################################
##########################################################################################################
def download_all(List_box,FOLDER):
    pdf_list= List_box.get (0,tkinter.END)
    if not os.path.exists(FOLDER):
        try:
            os.makedirs(FOLDER)
        except:
            return
    for x in pdf_list:
        if x != None:
            threading.Thread(target=download_pdf_from_link,args=(x,FOLDER)).start()



##########################################################################################################
##########################################################################################################
##
##              This function is for the GUI download selection button B2 it grabs all of the links
##              selected in ListBox  Lb1 and puts them in designated folder correspoding to user's query
##
##########################################################################################################
##########################################################################################################
def download_selection(List_box,FOLDER):
    pdf_list_index= List_box.curselection()
    pdf_list = []
    for x in pdf_list_index:
        pdf_list.append(List_box.get(x))
    if not os.path.exists(FOLDER):
        try:
            os.makedirs(FOLDER)
        except:
            return
    for x in pdf_list:
        if x != None:
            threading.Thread(target=download_pdf_from_link,args=(x,FOLDER)).start()

##########################################################################################################
##########################################################################################################
##
##            This function create the main GUI window and populates it with the widgets such as buttons,  
##            labels, listbox, and entry box. 
##
##########################################################################################################
##########################################################################################################
def GUI_ENTRY():
    top = tkinter.Tk()
    top.title("PDF_GRABBER")
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

    top.mainloop()



##THE FOLLOWING LINE LAUNCHES THE GUI_ENTRY FUNCTION THERBY STARTING THE SCRIPT
GUI_ENTRY()


