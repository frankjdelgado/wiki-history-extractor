# wiki-history-extractor
A wikipedia history revision extractor through web spiders and API usage


### Scraper
_Note: Currently the code only extract revisions from this [url](https://en.wikipedia.org/w/index.php?title=Malazan_Book_of_the_Fallen&action=history)_
  * Navigate to /scraper
  * Install requeriments `pip install -r requirements.txt`
  * Run `scrapy crawl wikis`
  
The extracted revision will be saved in scraper/revisions.json
