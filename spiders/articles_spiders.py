import scrapy
import html2text

class MPRSpider(scrapy.Spider):
    name = "articles_mpr"
    start_urls = ["http://www.mespropresrecherches.com/"]

    def parse(self, response):
        articles_urls = response.css("div.content-thumb a::attr(href)").extract()
        lead_title_url = response.css(".content-lead-title a::attr(href)").extract_first()
        if lead_title_url:
            articles_urls.append(lead_title_url)
        for href in articles_urls:
            yield response.follow(href, self.parse_article)
        next_page_href = response.css("a.next::attr(href)").extract_first()
        if next_page_href:
            yield response.follow(next_page_href, self.parse)

    def parse_article(self, response):
        title = response.css(".entry-title::text").extract_first()
        author = response.css(".author a::text").extract_first()
        tags = response.css(".entry-tags a::text").extract()
        text = response.css(".entry-content").extract_first()
        converter = html2text.HTML2Text()
        converter.ignore_links = True
        converter.ignore_images = True
        converter.ignore_emphasis = True
        converter.ignore_tables = True
        text = converter.handle(text)
        yield {
            "title": title,
            "author": author,
            "tags": tags,
            "text": text
        }


class StopMensongesSpider(scrapy.Spider):
    name = "articles_stopmensonges"
    start_urls = [f"http://stopmensonges.com/category/categories/derniers-articles-postes/page/{i}/"
                  for i in range(1, 558)]

    def parse(self, response):
        articles_urls = response.css(".entry-title a::attr(href)").extract()
        for href in articles_urls:
            yield response.follow(href, self.parse_article)

    def parse_article(self, response):
        title = response.css(".entry-title::text").extract_first()
        author = response.css(".td-author-name a::text").extract_first()
        tags = response.css(".td-tags a::text").extract()
        converter = html2text.HTML2Text()
        converter.ignore_tables = True
        converter.ignore_emphasis = True
        converter.ignore_links = True
        converter.ignore_images = True
        text = converter.handle(response.css(".td-post-content").extract_first())

        yield {
            "author":author,
            "title": title,
            "tags": tags,
            "text":text
        }


class ESMSpider(scrapy.Spider):
    name = "articles_esm"
    start_urls = ["https://www.espritsciencemetaphysiques.com/"]

    def parse(self, response):
        articles_urls = response.css(".entry-title a::attr(href)").extract()
        for href in articles_urls:
            yield response.follow(href, self.parse_article)

        previous = response.css(".nav-previous a::attr(href)").extract_first()
        if previous:
            yield response.follow(previous, self.parse)

    def parse_article(self, response):
        title = response.css(".entry-title::text").extract_first()
        author = response.css(".author a::text").extract_first()
        tags = []
        converter = html2text.HTML2Text()
        converter.ignore_tables = True
        converter.ignore_emphasis = True
        converter.ignore_links = True
        converter.ignore_images = True
        text = converter.handle(response.css(".entry-content").extract_first())
        yield {
            "author": author,
            "title": title,
            "tags": tags,
            "text": text
        }



class WikistrikeSpider(scrapy.Spider):
    name = "articles_wikistrike"
    start_urls = ["http://www.wikistrike.com/"]

    def parse(self, response):
        articles_urls = response.css(".post-title a::attr(href)").extract()
        for href in articles_urls:
            yield response.follow(href, self.parse_article)

        previous = response.css("a.ob-page-next::attr(href)").extract_first()
        if previous:
            yield response.follow(previous, self.parse)

    def parse_article(self, response):
        title = response.css(".post-title::text").extract_first()
        author = ""
        tags = response.css(".meta a::attr(title)").extract()
        converter = html2text.HTML2Text()
        converter.ignore_tables = True
        converter.ignore_emphasis = True
        converter.ignore_links = True
        converter.ignore_images = True
        text = converter.handle(response.css(".ob-section-html").extract_first())
        converter.close()
        yield {
            "author": author,
            "title": title,
            "tags": tags,
            "text": text
        }


