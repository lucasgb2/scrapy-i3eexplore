# -*- coding: utf-8 -*-

class Paper():
    def __init__(self, linkPaper):
        self.linkPaper = linkPaper
        self.doi = ''
        self.titlePaper = ''
        self.abstract = ''
        self.author = []
        self.conference = ''
        
    def __repr__(self):
        return 'Title: %s Link: %s' % (self.titlePaper, self.linkPaper)
