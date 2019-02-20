import httplib2
from bs4 import BeautifulSoup
from nltk import stem, tokenize
from nltk.corpus import wordnet

focused_links = []
outgoing_dict = {}
incoming_dict = {}

#dict where key is URL in BFS.txt and value is the canonical link
true_link_dict = {}

#Stemmer object for text cleaning
stemmer = stem.PorterStemmer()

#convert the string into lowercase and do stemming
def clean_text(content):
    lowercase_content = tokenize.wordpunct_tokenize(content.lower().strip())
    return ' '.join([stemmer.stem(word) for word in lowercase_content])

#find synonyms of the keyword so that they can also be searched for occurrences
#also finds synonyms of the words in a phrase
def find_synonyms(keyword):
    synonyms = []
    keyword_list = keyword.split('_')
    for j in range(0,len(keyword_list)):
        keyword_list[j] = ''.join(e for e in keyword_list[j] if e.isalnum())
    for i in range(0,len(keyword_list)):
        for synonym in wordnet.synsets(keyword_list[i]): 
            for l in synonym.lemmas(): 
                synonyms.append(l.name())  
    return list(synonyms)

#checks similarity between two words using Wup similarity
def check_similarity(list1,list2):
    list = []
    for word1 in list1:
        for word2 in list2:
            wordFromList1 = wordnet.synsets(word1)
            wordFromList2 = wordnet.synsets(word2)
            if wordFromList1 and wordFromList2: 
                for i in range(len(wordFromList1)):
                    for j in range(len(wordFromList2)):
                        s = wordFromList1[i].wup_similarity(wordFromList2[j])
                        if s == None:
                            s = 0.00
                        list.append(s)
    if len(list) > 0 and max(list) > 0.6:
        return True
    else:
        return False
    
#Function to get the docID from link   
def get_node_name(url):
    if(type(url) == str):
        return url.split('https://en.wikipedia.org/wiki/',1)[1]

#function to find relavant links based on similarity 
def is_link_focused(keyword, url):
    docID_variations = []
    docID = get_node_name(url)
    cleaned_docID  = clean_text(docID)
    docID_variations = find_synonyms(cleaned_docID)
    docID_variations.append(cleaned_docID) 
    
    keyword_variations = []
    keyword_docID = get_node_name(keyword)
    cleaned_keyword_docID = clean_text(keyword_docID)
    keyword_variations = find_synonyms(cleaned_keyword_docID)
    keyword_variations.append(cleaned_keyword_docID)
    if len(list(set(keyword_variations) & set(docID_variations))) > 3 or check_similarity(keyword_variations,docID_variations):
        return True
    else:
        return False
     
    
#Function to get the fetch outgoing links of a link
def get_links(soup):
    urls = []
    outgoing_links = []
    for div in soup.find_all("div", {"class":"mw-body-content"}):
        for link in div.select("a"):
            if link.has_attr('href'):
                if link['href'].startswith("/wiki/") and ":" not in link['href'] and "Main_Page" not in link['href']: 
                    urls.append(link['href'])
    urls = ['https://en.wikipedia.org' + s for s in urls]
    urls = set(urls)
    for s in urls:
        if s in focused_links:
            outgoing_links.append(get_node_name(s))
    return outgoing_links  

#Function to convert FOCUSED.txt to a list
def get_focused_links():
    with open('FOCUSED.txt','r') as f:
        for url in f:
            url = url.strip()
            focused_links.append(url)
            
#Function to create a dictionary of links with edges as outgoing links
def get_outgoing_dict():          
     with open('FOCUSED.txt','r') as f:
            for url in f:
                 url = url.strip()
                 http = httplib2.Http()
                 status, response = http.request(url)
                 soup = BeautifulSoup(response, "html.parser")
                 canonical = soup.find('link', {'rel': 'canonical'})
                 true_link = canonical['href'] 
                 if true_link not in true_link_dict.values():
                         true_link_dict.setdefault(url,[]).append(true_link)
                         outgoing_links = get_links(soup)
                         node_name = get_node_name(url)
                         for l in outgoing_links:
                             outgoing_dict.setdefault(node_name,[]).append(l)

#Function which checks if a link is redirected link
#returns the original link if it is passed a redirected link                     
def check_if_redirected_link(node):
     url = 'https://en.wikipedia.org/wiki/' + node
     http = httplib2.Http()
     status, response = http.request(url)
     soup = BeautifulSoup(response, "html.parser")
     canonical = soup.find('link', {'rel': 'canonical'})
     true_link = canonical['href'] 
     for k, v in true_link_dict.items():    # for name, age in dictionary.iteritems():  (for Python 2.x)
         if v == true_link:
             return k      

#Function to find the graph with edges as incoming links
#Outgoing links fetched using get_outgoing_dict() may contain redirected links
#This function takes care of those redirected links            
def find_incoming_graph():
    for key in outgoing_dict.keys():    
        value = outgoing_dict[key]
        if type(value) != list:
            complete_url = 'https://en.wikipedia.org/wiki/' + value
            if complete_url not in true_link_dict.keys():
                actual_url = check_if_redirected_link(value) 
                if(actual_url):
                    outgoing_dict[key].append(get_node_name(actual_url))
                else:
                    outgoing_dict[key].remove(value)
        if type(value) == list:
            for i in value:
                complete_link = 'https://en.wikipedia.org/wiki/' + i
                if complete_link not in true_link_dict.keys():
                    actual_url = check_if_redirected_link(i) 
                    if(actual_url):
                        if get_node_name(actual_url) not in value:
                            outgoing_dict[key].remove(i)
                            outgoing_dict[key].append(get_node_name(actual_url))
                        else:
                            outgoing_dict[key].remove(i)
                    else:
                         outgoing_dict[key].remove(i)
                         
    for k,value_list in outgoing_dict.items():
           if type(value_list) == str:
               incoming_dict.setdefault(value_list,[]).append(k)
           else:
               if type(value_list) == list:
                    for element in value_list:
                        incoming_dict.setdefault(element,[]).append(k)
           
def get_graph_stats():
    nodes_without_incoming = []
    nodes_without_outgoing = []
    incoming_links = list(incoming_dict.keys())
    outgoing_links = list(outgoing_dict.keys())
    focused_nodes = []
    for link in focused_links:
        focused_nodes.append(get_node_name(link))
    for node in focused_nodes:
        if node not in incoming_links:
            nodes_without_incoming.append(node)
    for node in focused_nodes:
        if node not in outgoing_links:
            nodes_without_outgoing.append(node)     
    maximum_indegree = 0
    for key in incoming_dict.keys():
        if maximum_indegree < len(incoming_dict[key]):
            maximum_indegree = len(incoming_dict[key])
    maximum_outdegree = 0
    for key in outgoing_dict.keys():
        if maximum_outdegree < len(outgoing_dict[key]):
            maximum_outdegree = len(outgoing_dict[key])
    print("The number of pages with no in-links: " , len(nodes_without_incoming))
    print("The number of pages with no out-links: " , len(nodes_without_outgoing))
    print("Maximum in-degree" , maximum_indegree)
    print("Maximum out-degree" , maximum_outdegree)     
    
#Function to create graph text file                
def create_graph_file():
    with open('G2.txt','w') as file:
        file.write("G2 = { \n")
        for k in sorted (incoming_dict.keys()):
            file.write("'%s':'%s', \n" % (k, incoming_dict[k]))
        file.write("}")
        

get_focused_links()               
get_outgoing_dict()
find_incoming_graph()
create_graph_file()
get_graph_stats()


        
