Project by Karim Rifai


Instruction for use in command line.
1. Open project folder in command line by using cd
2. Invoke python interpreter by typing Python
3. Import the modules by typing:
	>>> import crawler
	>>> import searchdata
	>>> import search

4. Start crawl by typing:
	>>> crawler.crawl(seed)		#Seed is the url which the crawler starts at, string

5. Search the data from crawling with the following functions:
	>>> search.search(phrase, boost)	#(string, boolean)
	>>> searchdata.get_outgoing_links(URL)	#(string)
	>>> searchdata.get_incoming_links(URL)	#(string)
	>>> searchdata.get_page_rank(URL)	#(string)
	>>> searchdata.get_idf(word)		#(string)
	>>> searchdata.get_tf(URL, word)	#(string, string)
	>>> searchdata.get_tf_idf(URL, word)	#(string, string)

7. Return to step 4. to crawl at another seed
8. Type exit() to exit
