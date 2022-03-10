from bs4 import BeautifulSoup
import requests as rq
import re

class Content:

    def __init__(self, url, title, body) -> None:
        self.title = title
        self.body = body
        self.url = url
        

    def print(self):
        """
        Flexible printing function controls output
        """
        print("URL: {}".format(self.url))
        print("TITLE: {}".format(self.title))
        print("BODY:\n{}".format(self.body))


class Website:
    """
    Contains information about website structure
    """
    
    def __init__(self, name, url, targetPattern, absoluteUrl, titleTag, bodyTag) -> None:
        self.name = name
        self.url = url
        self.targetPattern = targetPattern
        self.absoluteUrl = absoluteUrl
        self.titleTag = titleTag
        self.bodyTag = bodyTag

        
class Crawler:

    def __init__(self, site) -> None:
        self.site = site
        self.visited = []

    def getPage(self, url):
        try:
            req = rq.get(url)
        except rq.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text, 'lxml')
    
    def safeGet(self, pageObj, selector):
        selectedElems = pageObj.select(selector)
        if selectedElems is not None and len(selectedElems) > 0:
            return "\n".join([elem.get_text() for elem in selectedElems])
        return ''

    def parse(self, url):
        print("parsing url: " + url)
        bs = self.getPage(url)
        if bs is not None:
            title = self.safeGet(bs, self.site.titleTag)
            body = self.safeGet(bs, self.site.bodyTag)
            if title == '':
                print("Title is none")
            if body == '':
                print("Body is none")
            if title != '' and body != '':
                content = Content(url, title, body)
                content.print()

    def crawl(self):
        """
        Get pages from website home page
        """
        bs = self.getPage(self.site.url)
        targetPages = bs.find_all("a", href=re.compile(self.site.targetPattern))
        for targetPage in targetPages:
            targetPage = targetPage.attrs["href"]
            if targetPage not in self.visited:
                self.visited.append(targetPage)
                if not self.site.absoluteUrl:
                    targetPage = '{}{}'.format(self.site.url, targetPage)
                self.parse(targetPage)


if __name__ == "__main__":

    print("Running script now!")
    reuters = Website("Reuters", 'https://www.reuters.com', '^(/world/)', False, 'h1', 'div.article-body__content__3VtU3')
    crawler = Crawler(reuters)
    crawler.crawl()
    print("Finished running script!")

