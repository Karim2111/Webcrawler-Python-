import json
import math

def get_outgoing_links(URL):
    crawl_data = get_crawl_data()
    if URL in crawl_data:
        return crawl_data[URL]['outgoing']
    return None
    
def get_incoming_links(URL):
    crawl_data = get_crawl_data()
    if URL in crawl_data:
        return crawl_data[URL]['incoming']
    return None
    
def get_page_rank(URL):
    crawl_data = get_crawl_data()
    if URL in crawl_data:
        return crawl_data[URL]['pagerank']
    return -1
    
def get_idf(word):
    idf_data = get_idf_data()
    if word in idf_data:
        return idf_data[word]
    return 0
    
    
def get_tf(URL, word):
    crawl_data = get_crawl_data()
    if URL in crawl_data:
        if word in crawl_data[URL]['tf']:
            return crawl_data[URL]['tf'][word]
    return 0

def get_tf_idf(URL, word):
    tf = get_tf(URL, word)
    idf = get_idf(word)
    return (math.log2(1 + tf) * idf)

def get_crawl_data():
    with open('crawl/crawl data.json', 'r') as f:
        return json.loads(f.read())

def get_idf_data():
    with open('crawl/idf.json', 'r') as f:
        return json.loads(f.read())