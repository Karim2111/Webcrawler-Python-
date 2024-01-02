import searchdata
import math

def search(phrase, boost):
    global crawl_data, idf_data
    phrase = phrase.lower().split()
    
    crawl_data = searchdata.get_crawl_data()
    idf_data = searchdata.get_idf_data()

    query_vector = get_query_vector(phrase)

    search_score = {} # {url : search score}
    for url in crawl_data:
        search_score.update(get_cosine_similarity(query_vector, url, boost))
    
    search_score = sorted(search_score.items(), key=lambda x:x[1], reverse = True)
    top10 = [{'url' : element[0], 'title' : crawl_data[(element[0])]['title'], 'score' : element[1]} for element in search_score[:10]]
    return top10

def get_query_vector(phrase):
    query_vector = {}
    total_words_in_phrase = len(phrase)
    unique_words = list(set(phrase))
    for word in unique_words:
        if word in idf_data:
            idf = idf_data[word]
        else:
            idf = 0
        tf = phrase.count(word) / total_words_in_phrase
        query_vector[word] = (math.log2(1 + tf) * idf)
    return query_vector

def get_cosine_similarity(query_vector, url, boost):
    numerator = 0
    left_denominator = 0
    right_denominator = 0
    for term in query_vector:   
        numerator += query_vector[term] * get_tf_idf(url, term)
        left_denominator += query_vector[term] * query_vector[term]
        right_denominator += get_tf_idf(url, term) * get_tf_idf(url, term)
    left_denominator = math.sqrt(left_denominator)
    right_denominator = math.sqrt(right_denominator)
    if numerator == 0:
        result = 0
    else:
        result = (numerator / (left_denominator * right_denominator))
        if boost:
            result = result * crawl_data[url]['pagerank']
    return {url : result}


def get_idf(word):
    if word in idf_data:
        return idf_data[word]
    return 0
    
def get_tf(URL, word):
    if URL in crawl_data:
        if word in crawl_data[URL]['tf']:
            return crawl_data[URL]['tf'][word]
    return 0

def get_tf_idf(URL, word):
    tf = get_tf(URL, word)
    idf = get_idf(word)
    return (math.log2(1 + tf) * idf)