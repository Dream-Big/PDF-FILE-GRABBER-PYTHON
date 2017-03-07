##                          This program was written by Shady Salaheldin
##                                  shady.a.salaheldin@gmail.com
##                                          v0.0.1.0
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



import urllib
import os
import requests
import xml.dom.minidom

url_endpoint = 'https://www.duckduckgo.com/html'
keepsearching = True
while(keepsearching):
    
    user_query = str(input("Please Enter Query : "))
    mydict = {'q': str("'"+str(user_query)+"'")}
    resp = requests.get(url_endpoint, params=mydict)

    dom = xml.dom.minidom.parseString(resp.text)
    list_of_links = dom.getElementsByTagName('a')

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
            try:
                url = x
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}
                response = requests.get(url,headers=headers)
                book_name = url.split('/')[-1]
                with open(user_query+'/'+book_name, 'wb') as f:
                    f.write(response.content)
            except:
                print(str(x)+" could not be downloaded")



    continue_searching_prompt = str(input("Continue searching? (y/n) "))
    if continue_searching_prompt == "n":
        keepsearching = False
