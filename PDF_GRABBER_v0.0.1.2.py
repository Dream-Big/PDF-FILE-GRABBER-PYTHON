##                          This program was written by Shady Salaheldin
##                                  shady.a.salaheldin@gmail.com
##                                          v0.0.1.2
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


import threading
#import time
import urllib
import os
import requests
import xml.dom.minidom

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

##def create_DND_FILE(DND_LIST,FOLDER_NAME):
##    try:
##        PATH_FINAL = str(FOLDER_NAME+'/00000000--DND.txt')
##        with open(PATH_FINAL, 'w') as f:
##            for x in DND_LIST:
##                f.write(str(x)+'\n')
##        return True
##    except:
##        return False
##
##def create_DL_FILE(DL_LIST,FOLDER_NAME):
##    try:
##        PATH_FINAL = str(FOLDER_NAME+'/00000000-DL.txt')
##        with open(PATH_FINAL, 'w') as f:
##            for x in DL_LIST:
##                f.write(str(x)+'\n')
##        return True
##    except:
##        return False



def DO_QUERY(query_string):
    url_endpoint = 'https://www.duckduckgo.com/html'
    user_query = query_string[:-1]
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
            elif not pdf_list: pdf_list.append(str(urllib.parse.unquote(link)))

        ###################################################################################################
        pdf_list.pop(0)
        #######not sure why the list is created with 1 extra blank item in beginning so i am ridding of it.
        
        #for x in pdf_list:
        #    print(str(x) + "\n")


        if not os.path.exists(user_query):
            os.makedirs(user_query)
        for x in pdf_list:
            threading.Thread(target=download_pdf_from_link,args=(x,user_query)).start()
##        for x in pdf_list:
##            if(not (threading.Thread(target=download_pdf_from_link,args=(x,user_query)).start())):
##                DND_LIST.append(str(x))
##            else: DL_LIST.append(str(x))
        ##### need to add a way to ensure all files have been processed befor creat_DND_FILE  is called
        #create_DND_FILE(DND_LIST,user_query)
        #create_DL_FILE(DL_LIST,user_query)

                  
    except:
        prin(str(user_query))
        print("An error occured - please try again.")

    
def READ_QUERY_FROM_FILE(FILE_NAME):
    try:
        with open(FILE_NAME, 'r') as f:
            query_strings = f.readlines()
        for x in query_strings:
            threading.Thread(target=DO_QUERY,args=(x,)).start()
        return True
    except:
        print("could not open file")
        return False





def USER_ENTERS_QUERY():
    url_endpoint = 'https://www.duckduckgo.com/html'
    user_query = str(input("Please Enter Query : "))
    mydict = {'q': str("'"+str(user_query)+"'")}
    resp = requests.get(url_endpoint, params=mydict)
    try:
        dom = xml.dom.minidom.parseString(resp.text)
        list_of_links = dom.getElementsByTagName('a')

##        DL_LIST = []
##        DND_LIST = []
        pdf_list = []

        for x in list_of_links:
            link=x.getAttribute('href')
            link=link.split('=')[-1]
            if str(link)[-4:] == ".pdf" and pdf_list and str(pdf_list[len(pdf_list)-1]) != str(str(urllib.parse.unquote(link))):
                pdf_list.append(str(urllib.parse.unquote(link)))
            elif not pdf_list: pdf_list.append(str(urllib.parse.unquote(link)))

        ###################################################################################################
        pdf_list.pop(0)
        #######not sure why the list is created with 1 extra blank item in beginning so i am ridding of it.
        
        for x in pdf_list:
            print(str(x))

        download_prompt = str(input("Download all? (y/n) "))

        if download_prompt == "y":
            if not os.path.exists(user_query):
                os.makedirs(user_query)
            for x in pdf_list:
                threading.Thread(target=download_pdf_from_link,args=(x,user_query)).start()
##                if(not (threading.Thread(target=download_pdf_from_link,args=(x,user_query)).start())):
##                   DND_LIST.append(str(x))
##                else: DL_LIST.append(str(x))
##            ##### need to add a way to ensure all files have been processed befor creat_DND_FILE  is called
##            create_DND_FILE(DND_LIST,user_query)
##            create_DL_FILE(DL_LIST,user_query)
##            ##### need to add a way to ensure all files have been processed befor creat_DND_FILE  is called
    except:
        print("An error occured - please try again.")



def PROMPT_ENTRY():
    print("Hello, and Thank You for choosing this software!\n")
    keepsearching = True
    while(keepsearching):
        SELECT_MODE = ""
        while(SELECT_MODE != "F" and SELECT_MODE != "f" and SELECT_MODE != "M" and SELECT_MODE != "m"):
            SELECT_MODE = str(input("Please Select FILE MODE or MANUAL INPUT MODE: (F/M)"))
        if (SELECT_MODE == "F" or SELECT_MODE == "f") :
            FILE_NAME = str(input("Please Enter File Name ending in .txt:"))
            while (not os.path.exists(FILE_NAME) and FILE_NAME != "Q" and FILE_NAME !="q"):
                print(FILE_NAME+" Does Not Exist!\n")
                FILE_NAME = str(input("Please Enter Valid File Name ending in .txt or Q to exit File Mode:"))
            if  (FILE_NAME != "Q" and FILE_NAME != 'q'):
                READ_QUERY_FROM_FILE(FILE_NAME)
        elif (SELECT_MODE == "M" or SELECT_MODE == "m" ):
            USER_ENTERS_QUERY()
        SELECT_MODE = ""
        continue_searching_prompt = str(input("Continue searching? (y/n) "))
        if continue_searching_prompt == "n":
            keepsearching = False




PROMPT_ENTRY()
