import webdev
import filehelp
import json
import math
import matmult

#seed = 'http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html'

#format of crawl_data dictionary
#crawl_data = {url : {
#                       'title' : '',
#                       'tf' : {word1 : tf_word1},
#                       'outgoing links' : [],
#                       'incoming links' : [],
#                       'pagerank' : float,
#                       }
#               }

def crawl(seed):
    queue = [seed]
    visited = set()
    crawl_data = {}
    filehelp.clear_directory('crawl')

    
    while queue:
        current_url = queue.pop()
        visited.add(current_url)
        page = webdev.read_url(current_url)

        title = get_title(page)
        outgoing_links = relative_to_absolute_link(get_outgoing_links(page, title), current_url)
        word_frequency = get_word_frequency(page)
        tf = calculate_tf(word_frequency)

        crawl_data[current_url] = {}
        crawl_data[current_url]['title'] = title
        crawl_data[current_url]['outgoing'] = outgoing_links
        crawl_data[current_url]['word frequency'] = word_frequency
        crawl_data[current_url]['tf'] = tf

        queue_outgoing_links(outgoing_links, visited, queue)

    incoming_links = get_incoming_links(crawl_data)
    pagerank = get_pagerank(crawl_data)
    idf = get_idf(crawl_data)

    for url in crawl_data:
        crawl_data[url]['incoming'] = incoming_links[url]
        crawl_data[url]['pagerank'] = pagerank[url]
        del crawl_data[url]['word frequency']
    
    filehelp.create_file('crawl/crawl data.json', json.dumps(crawl_data))
    filehelp.create_file('crawl/idf.json', json.dumps(idf))

    return len(visited)

def get_idf(crawl_data):
    idf = {} # {word : idf}
    total_documents = len(crawl_data)
    document_frequency = {} # {word : # of documents word appears in}
    for document in crawl_data:
        for word in crawl_data[document]['word frequency']:
            if word not in document_frequency:
                document_frequency[word] = 0
            document_frequency[word] += 1
    for word in document_frequency:
        idf[word] = math.log2(total_documents / (1 + document_frequency[word]))
    return idf

def get_incoming_links(crawl_data):
    incoming_links = {url : [] for url in crawl_data} #url : [incoming links]
    for url in crawl_data:
        for outgoing_link in crawl_data[url]['outgoing']:
            incoming_links[outgoing_link].append(url)
    return incoming_links

def get_pagerank(crawl_data):
    adjacency_matrix = []
    alpha = 0.1
    N = len(crawl_data)
    for node_i in crawl_data:
        adjacency_matrix.append([int(node_j in crawl_data[node_i]['outgoing']) for node_j in crawl_data])
    for index, row in enumerate(adjacency_matrix):
        number_ones = sum(row)
        adjacency_matrix[index] = [(1-alpha) * (item/number_ones) + (alpha/N) for item in row]

    previous = [[1/N for i in range(N)]]
    result = matmult.mult_matrix(previous, adjacency_matrix)
    while matmult.euclidean_dist(previous, result) > 0.0001:
        previous = result
        result = matmult.mult_matrix(result, adjacency_matrix)

    pagerank = {}
    for index, url in enumerate(crawl_data):
        pagerank[url] = result[0][index]

    return pagerank

def get_title(html):
    opening_tag = '<title>'
    closing_tag = '</title>'
    start_index = html.find(opening_tag) + len(opening_tag)
    end_index = html.find(closing_tag)
    return html[start_index:end_index]

def get_word_frequency(html):
    opening_tag = '<p>'
    closing_tag = '</p>'
    words = []
    while True:
        start_index = html.find(opening_tag)
        if start_index == -1:
            break
        start_index += len(opening_tag)
        end_index = html.find(closing_tag)
        words += html[start_index:end_index].split()
        html = html[end_index + len(closing_tag):]

    word_frequency = {}
    for word in words:
        if word not in word_frequency:
            word_frequency[word] = 0
        word_frequency[word] += 1
    return word_frequency

def calculate_tf(word_frequency):
    tf = {}
    total_words = sum(word_frequency.values())
    for word in word_frequency:
        tf[word] = word_frequency[word] / total_words
    return tf

def get_outgoing_links(html, title):
    opening_tag = '<a href="'
    closing_tag = '">'
    outgoing_links = set()
    while True:
        start_index = html.find(opening_tag) + len(opening_tag)
        if start_index == -1 + len(opening_tag):
            break
        end_index = html.find(closing_tag)
        outgoing_links.add(html[start_index:end_index])
        html = html[end_index + len(closing_tag):]
    return outgoing_links

def relative_to_absolute_link(links, current_url):
    absolute_links = []
    base_url = current_url[:current_url.rfind('/')+1]
    for link in links:
        if link[:2] == './':
            absolute_links.append(base_url + link[2:])
        else:
            absolute_links.append(link)
    return absolute_links

def queue_outgoing_links(outgoing_links, visited, queue):
    for link in outgoing_links:
        if link in visited:
            continue
        queue.append(link)
        visited.add(link)
    return



#crawl(seed)