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

https://en.wikipedia.org/w/api.php?action=query&titles=Malazan%20Book%20of%20the%20Fallen&prop=revisions&rvprop=ids|flags|timestamp|user|flags|user|userid|size|sha1|contentmodel|comment|parsedcomment|content|tags&format=jsonfm&rvlimit=50
