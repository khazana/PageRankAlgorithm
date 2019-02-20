from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from nltk import tokenize
import string
import itertools
from nltk import ngrams
from collections import Counter
import os
import matplotlib.pyplot as plt


#maintains trigram dictionay
trigram_list = Counter()

trigrams = []

#contains a list of URLS after pruning redirected and duplicate links fromm BFS.txt
unique_urls = []

#Function to create the corpus for a document
#Extracts required content and tokenizes it
#Removes punctuation except '-'
#Saves the corpus in 'ParsedTextFiles', replace with your directory
def process_text(rawfile):
    fh = open(rawfile,"rb")
    contents = fh.read().decode(errors='replace')
    all_text = []
    soup = BeautifulSoup(contents,features="lxml")
    if soup.select(".firstHeading"):
         first_heading =  soup.select(".firstHeading")[0].text
         first_heading = tokenize.wordpunct_tokenize(first_heading.lower().strip())
         all_text.append(first_heading)
    soup = soup.find("div", {"class":"mw-content-ltr"})
    if soup.find('div', id="toc"):
        soup.find('div', id="toc").decompose()
    if soup.find('div', {"class":"reflist"}):
        soup.find('div', {"class":"reflist"}).decompose()
    if soup.find_all("div", {'class':'navbox'}): 
        for div in soup.find_all("div", {'class':'navbox'}): 
            div.decompose()
    content = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'p','li'])
    file_name = rawfile.split('/Users/fathimakhazana/Documents/IRHW2/RawTextFiles/')[1]
    file_name = file_name.split('_raw.txt')[0]
    file_name = file_name + '.txt'
    if '\\n' in file_name:
        file_name = file_name.replace('\\n','')
    if '/' in file_name:
        file_name = file_name.replace('/','-')
    with open('/Users/fathimakhazana/Documents/IRHW2/ParsedTextFiles/' + file_name, 'w') as f:
        for header in content:
            text = header.text
            text = text.replace('[edit]', '')
            text = re.sub(r"\[\d+", " ", text)
            remove = string.punctuation
            remove = remove.replace("-", "")
            pattern = r"[{}]".format(remove)
            text = re.sub(pattern, "", text)            
            text = tokenize.wordpunct_tokenize(text.lower().strip())
            all_text.append(text)
        new_list = list(itertools.chain.from_iterable(all_text))
        f.write("%s\n" % new_list)
        trigrams_list = ngrams(new_list,3)
        for trigram in trigrams_list :
            trigram_list[trigram] += 1
            

#Function to download the pages in BFS.txt 
#Saves the raw text in 'RawTextFiles', replace with your directory
def download_pages():
    with open('BFS.txt','r') as f:
        for url in f:
             soup = BeautifulSoup(urlopen(url),features="lxml")
             canonical = soup.find('link', {'rel': 'canonical'})
             true_link = canonical['href'] 
             if true_link not in unique_urls:
                 unique_urls.append(url)
                 url = url.strip()
                 file_name = url.split('https://en.wikipedia.org/wiki/',1)[1]
                 if '\\n' in file_name:
                     file_name = file_name.replace('\\n','')
                 if '/' in file_name:
                     file_name = file_name.replace('/','-')       
                 with open('/Users/fathimakhazana/Documents/IRHW2/RawTextFiles/' + file_name + '_raw.txt', 'a') as output:
                     output.write("%s\n" % soup)


#Function to create the trigram dictionary    
def create_trigrams_dict():
    files = [i for i in os.listdir('/Users/fathimakhazana/Documents/IRHW2/RawTextFiles/') if i.endswith(".txt")]
    for file in files:
        process_text('/Users/fathimakhazana/Documents/IRHW2/RawTextFiles/' + file)

#Function to write the trigram dictionary to a text file    
def write_trigrams_file():
    trigram_dict = dict(trigram_list)
    with open('Trigrams.txt','w') as file:
        file.write("Trigrams = { \n")
        for k in trigram_dict.keys():
            file.write("'%s':'%s', \n" % (k, trigram_dict[k]))
        file.write("}") 

#Plots Zips graph           
def plot_rank_graph():
    w = 6
    h = 3
    d = 70
    plt.figure(figsize=(w, h), dpi=d)
    x = list(range(1,len(trigram_list)+1))
    y = [x[1] for x in trigram_list]
    plt.ylabel('Frequency')
    plt.xlabel('Rank')
    plt.loglog(x, y)
    plt.savefig("Zipf.png")
    

#Use this function to download the links in HTML format
#download_pages()
create_trigrams_dict()
trigram_list = trigram_list.most_common()
write_trigrams_file()
plot_rank_graph() 
    
    
        
