
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException   
from selenium.webdriver.common.by import By
from paper import Paper
import time

class CrawlerListIdeas():
    
    def __init__(self):
        self.urlRoot = 'https://ieeexplore.ieee.org/search/searchresult.jsp?action=search&newsearch=true&searchField=Search_All&matchBoolean=true&queryText=((lesion%20skin)%20AND%20deep%20learning)'
        self.urlCategoria = 'https://ieeexplore.ieee.org/search/searchresult.jsp?action=search&newsearch=true&searchField=Search_All&matchBoolean=true&queryText=((lesion%20skin)%20AND%20deep%20learning)'        
        self.currentPage = ''
        self.papers = []
        self.tagNameListIdeas = 'List-results-items'
        self.qtdePaginas = 1
        
    def acceptCookies(self, browser):
        time.sleep(1)
        button = browser.find_element_by_class_name('cc-compliance')        
        button.click()
        
        
    def getBrowser(self, link):
        browser = webdriver.Chrome(executable_path='chromedriver.exe')
        browser.get(link)
        
        return browser
        
    def getBrowserElementPresent(self, link, element):        
        browser = self.getBrowser(link)                
        element_present = EC.presence_of_element_located((By.CLASS_NAME, element))
        WebDriverWait(browser, 5).until(element_present)
        return  browser
    
    def clickButtonNextPage(self, browser):                        
        #quando nextAgain for False já leu todos os papers possíveis             
        try:
            button = browser.find_element_by_class_name('loadMore-btn')               
            button.click()
            nextAgain = True
        except:
            nextAgain = False
            
        return browser, nextAgain
    
    def getLinks(self, page):        
        soup = BeautifulSoup(page, 'html.parser')        
        div = soup.find_all("div", attrs={"class": "result-item-align"})     

        for p in div:                        
            paper = Paper('')
            for index, child in enumerate(p.findChildren('a')):
                if 'href' in child.attrs:                   
                    if 'document' in child['href']:
                        paper.linkPaper = 'https://ieeexplore.ieee.org'+child['href']
                        #este condição de checar se está vazio, é pois se haver outro
                        #document não deverá preencher
                        if paper.titlePaper == '':
                            paper.titlePaper = child.text
                        
                    if 'author' in child['href']:
                        paper.author.append(child.text)   
                        
                    if 'conhome' in child['href']:
                        paper.conference = child.text
                

                '''
                if 'class' in child.attrs:                               
                    if 'media' in child['class']:
                        urlIdeia = self.urlRoot + child['href'] 
                        print(urlIdeia)
                        self.papers.append(Ideia(urlIdeia))
                '''
            print(paper)
            self.papers.append(paper)
        return self.papers    
    
    
    def run(self):          
        for i in range(self.qtdePaginas):
            if self.currentPage == '':
                self.currentPage = self.urlCategoria
                browser = self.getBrowserElementPresent(self.currentPage, self.tagNameListIdeas)
                self.acceptCookies(browser)
                time.sleep(3)
                
                while True:
                    browser, nextAgain = self.clickButtonNextPage(browser)
                    time.sleep(4) 
                    print(nextAgain)
                    print(browser)
                    if nextAgain == False:
                        break
                    
                    
            else:
                browser = self.clickButtonNextPage(browser)
            self.getLinks(browser.page_source)   
            
        return self.papers       

    
class ScrapyPaper():
    
    def __init__(self, papers):
        self.papers = papers
        self.browserInit = None
        
    def getBrowser(self, link):
        if self.browserInit == None:
            self.browserInit = webdriver.Chrome(executable_path='chromedriver.exe')
        self.browserInit.get(link)        
        return self.browserInit        
        
    def getHtmlPage(self, link):
        browser = self.getBrowser(link)       
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'abstract-text'))
        WebDriverWait(browser, 5).until(element_present)          
        #page = urlopen(link).read()
        return browser.page_source
        
    def run(self):
        for paper in self.papers:            
            page = self.getHtmlPage(paper.linkPaper)            
            soup = BeautifulSoup(page, 'html.parser')
            div = soup.findAll("div", {"class": "abstract-text"})        
            if len(div) > 0:
                paper.abstract = div[0].get_text()
            '''
            for p in div:    
                paper.abstract = p.get_text()
                for index, child in enumerate(p.findChildren()):
                    
                    #print(p.text())
                    
                    if child.get_text() == 'Descrição do problema':                    
                        texto = p.findChildren()[index+1].get_text()
                        paper.problema = texto.strip()
                        
                    if child.get_text() == 'Solução Proposta':                    
                        texto = p.findChildren()[index+1].get_text()
                        paper.proposta = texto.strip()  
                        break
                        
                   '''
        return self.papers
    
            
if __name__ == '__main__':
    c = CrawlerListIdeas()
    papers = c.run()
   # print(papers)
    
    #p = Paper()
    #p.linkPaper = 'https://ieeexplore.ieee.org/document/8641815/'
    #papers = []
    #papers.append(p)
 #   for p in papers:
#        print(p)
    
    
 #   s = ScrapyIdea(papers)
#    papers = s.run()
