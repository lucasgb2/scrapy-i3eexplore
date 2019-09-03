
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import wordcloud 
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from urllib.request import urlopen
from crawler import CrawlerListIdeas, ScrapyPaper
from paper import Paper

#stopWords = set(stopwords.words("portuguese"))
stopWords = set(stopwords.words("english"))

c = CrawlerListIdeas()
papers = c.run()
    
s = ScrapyPaper(papers)
papers = s.run()
    
texto = ''
for i in papers:
    texto = texto + i.abstract
    
token = word_tokenize(texto)

filtered = []
for t in token:
    if t not in stopWords:
        filtered.append(t)

textoFiltered = ''
for word in filtered:
    textoFiltered += ' '+word+' '
        
wc = wordcloud.WordCloud().generate(textoFiltered)
plt.imshow(wc)
        