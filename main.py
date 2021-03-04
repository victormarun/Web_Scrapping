import pandas as pd
import numpy as np
import re
import urllib
from bs4 import BeautifulSoup
import copy
import urllib.request


def Get_Contacts_from_Page(urls=[]):
    if type(urls) is list:
        Dict_Result={}

        def visible(element):
            if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
                return False
            elif re.match('<!--.*-->', str(element.encode('utf-8'))):
                return False
            return True

        for url,i in zip(urls,range(len(urls))):
            Dict={} # create a temporary Dict
            html = urllib.request.urlopen(url) # request to web page html
            soup = BeautifulSoup(html) # convert hrtml to soup
            data = soup.findAll(text=True) # get all text from html

            html_texts = filter(visible, data) # get only visible data
            list_html_texts = list(html_texts) # convert to list
            result=[]
            regex = 're.sub("[^+0-9]", " ", x)' # regex to find number in text
            [ True if eval(regex).strip() in ['', None, ' ', '\n'] else result.append(eval(regex).strip()) for x in list_html_texts]
            df = pd.Series(data).to_frame() # convet html data to dataframe
            df.columns=["Data"]
            logo =""

            index = df['Data'].str.upper().str.contains('LOGO') # return index if contains LOGO
            if np.count_nonzero(index)>0:
                logo = df['Data'][index].values[0] #get Value
            else:
                index= df['Data'].str.upper().str.contains('.PNG')# return index if contains PNG
                if np.count_nonzero(index)>0:
                    logo = df['Data'][index].values[0] # get Value
            #save results
            Dict["phones"]=result
            Dict["logo"]=logo
            Dict["website"]=url
            Dict_Result[i]=copy.copy(Dict) # copy with different key in system
        return Dict_Result # return result



    else:
        return {}
Dict_Result={}

urls = pd.read_csv("websites.txt",header=None) # read input file
urls = urls[0].values.tolist() # convert to list
Dict_Result = Get_Contacts_from_Page(urls=urls) #call function
pd.DataFrame.from_dict(Dict_Result).to_json("Result.json") # save result in json file




