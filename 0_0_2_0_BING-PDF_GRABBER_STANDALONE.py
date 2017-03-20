##                          This program was written by Shady Salaheldin
##                                  shady.a.salaheldin@gmail.com
##                                          v0.0.2.0
##
##                                ~~!!! STAND ALONE GUI !!!~~
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##
##  This program searches the web using www.bing.com
##  and retrieves and stores all search results that end in .pdf which match the user's query.
##  The user decides how many pages to scrape.
##
##  The program them displays all of the links it has retrieved and asks the user if they want to download
##  all of the content or optionally select the content they want to download.
##
##  The content is then downloaded using Multi-threading to download and save the desired files in parellel.
##
##  if the user selects to download some or all files found, the program creates a folder named after the
##  query entered by the user, if it does not already exist.
##
##  The program then downloads and stores all pdf files in that new folder with the title of the pdf file
##  being same as original pdf file found on web.
##  (The program accounts for possible identical file names and doesn't overwrite,but rather makes copies)
##
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################



import tkinter
import threading
import urllib
import os
import requests



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
        return False

##########################################################################################################
##########################################################################################################
##
##              This function handles quering www.bing.com for provided query string
##              This fuction returns a list of all links that begin in http and end in .pdf
##
##########################################################################################################
##########################################################################################################
def DO_QUERY_FOR_GUI(query_string,page):
    url_endpoint = 'http://www.bing.com'
    user_query = query_string
    pdf_list = []
    if int(page)>=0 and int(page) <=1000:
        for xx in range(int(page)):
            mydict = {'q':str(user_query),'count':'50','first':str((xx*50)+1)}
            print(str(mydict))
            resp = requests.get(url_endpoint, params=mydict)
            try:
                href_blocks = str(resp.text).replace('"','\"').split('href=')
                list_of_links = []
                for x in href_blocks:
                    list_of_links.append(x.split('\"')[1])
                if list_of_links != None:
                    for link in list_of_links:
                        if str(link[:4]) =="http" :
                            if str(link)[-4:] == ".pdf":
                                pdf_list.append(str(link))
               
            except:
                print(str(user_query))
                print("An error occured - please try again.")
          
    return pdf_list  

##########################################################################################################
##########################################################################################################
##
##              This function is for the GUI submit button B1 it extracts query from Entry field E1
##              and calls DO_QUERY_FOR_GUI then passes the pdf list and list box Lb1 to create_list_box
##
##########################################################################################################
##########################################################################################################
def submit(E1_Query_Field,List_box,E2_Num_of_pages):
    List_box.delete(0,tkinter.END)
    pdf_list = DO_QUERY_FOR_GUI(E1_Query_Field.get(),E2_Num_of_pages.get())
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
    #print(str(pdf_list))
    for x in pdf_list:
        if x != None:
            List_box.insert(counter,str(x))
            counter = counter+1


##########################################################################################################
##########################################################################################################
##
##              This function is for the GUI download all button B3 it grabs all of the links in ListBox
##              Lb1, using Multi-threading, and puts them in designated folder correspoding to user's query
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
##              selected in ListBox  Lb1, using Multi-threading and puts them in designated folder
##              correspoding to user's query
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
    top.title("BING_PDF_GRABBER")
    top.resizable(width=False, height=False)
    top.geometry('{}x{}'.format(1280, 920))



    L1 = tkinter.Label(top, text="User Query: ")
    L1.pack(side = tkinter.TOP)
    E1 = tkinter.Entry(top, bd =5,width=100)
    E1.pack(side = tkinter.TOP)
    L2 = tkinter.Label(top, text="Number of search result pages to scrape: 50 links are per page by default scraping 2 pages would scrape 100 links for .pdf files. ")
    L2.pack(side = tkinter.TOP)
    E2 = tkinter.Entry(top, bd =5,width=100)
    E2.pack(side = tkinter.TOP)
    B1 = tkinter.Button(top, text ="Submit!", command= lambda: submit(E1,Lb1,E2))
    B1.pack(side = tkinter.TOP)
    Lb1 = tkinter.Listbox(top,height=40, width = 150,selectmode=tkinter.MULTIPLE,selectbackground='yellow')
    Lb1.pack(side = tkinter.TOP)
    B2 = tkinter.Button(top, text ="Download Selection!", command= lambda: download_selection(Lb1,E1.get()))
    B2.pack(side = tkinter.TOP)
    B3 = tkinter.Button(top, text ="Download ALL!", command= lambda: download_all(Lb1,E1.get()))
    B3.pack(side = tkinter.TOP)

    top.mainloop()



##          THE FOLLOWING LINE LAUNCHES THE GUI_ENTRY FUNCTION THERBY STARTING THE SCRIPT
GUI_ENTRY()


