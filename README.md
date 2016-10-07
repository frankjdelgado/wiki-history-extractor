# wiki-history-extractor
A wikipedia history revision extractor through web spiders and API usage


### Scraper
  * Install requeriments `pip install -r requirements.txt`
  * import class RevisionCrawler from revision_crawler.py
  * Initialize the crawler

    `urls = ['https://en.wikipedia.org/w/index.php?title=Malazan_Book_of_the_Fallen&action=history']`

    `crawler = RevisionCrawler(urls)`
  * Run it!

    `crawler.start()`

The extracted revision data will be saved into a file called revisions.json
