from bs4 import BeautifulSoup
import httplib2


BFS_links = []
outgoing_dict = {}
incoming_dict = {}

#dict where key is URL in BFS.txt and value is the canonical link
true_link_dict = {}

#Function to get the docID from link
def get_node_name(url):
    if(type(url) == str):
        return url.split('https://en.wikipedia.org/wiki/',1)[1]
    
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
        if s in BFS_links:
            outgoing_links.append(get_node_name(s))
    return outgoing_links 


#Function to convert BFS.txt to a list
def get_BFS_links():
 with open('BFS.txt','r') as f:
        for url in f:
            url = url.strip()
            BFS_links.append(url)
            

#Function to create a dictionary of links with edges as outgoing links
def get_outgoing_dict():          
    with open('BFS.txt','r') as f:
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
     for k, v in true_link_dict.items():   
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
    BFS_nodes = []
    for link in BFS_links:
        BFS_nodes.append(get_node_name(link))
    for node in BFS_nodes:
        if node not in incoming_links:
            nodes_without_incoming.append(node)
    for node in BFS_nodes:
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
    with open('G1.txt','w') as file:
        for k in sorted (incoming_dict.keys()):
            file.write("'%s':%s, \n" % (k, incoming_dict[k]))


get_BFS_links()               
get_outgoing_dict()
find_incoming_graph()
create_graph_file()
get_graph_stats()


                            
            
