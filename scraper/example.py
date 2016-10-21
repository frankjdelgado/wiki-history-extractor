from revision_crawler import RevisionCrawler


crawler = RevisionCrawler(urls=['https://en.wikipedia.org/w/index.php?title=Malazan_Book_of_the_Fallen&action=history'])
crawler.start()
