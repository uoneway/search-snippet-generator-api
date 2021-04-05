import newspaper  # from newspaper import Article, Config # https://newspaper.readthedocs.io/en/latest/   
from utils import __get_logger

logger = __get_logger()

"""
<Newspaper3k configuration options>
keep_article_html, default False, “set to True if you want to preserve html of body text”
http_success_only, default True, “set to False to capture non 2XX responses as well”
MIN_WORD_COUNT, default 300, “num of word tokens in article text”
MIN_SENT_COUNT, default 7, “num of sentence tokens”
MAX_TITLE, default 200, “num of chars in article title”
MAX_TEXT, default 100000, “num of chars in article text”
MAX_KEYWORDS, default 35, “num of keywords in article”
MAX_AUTHORS, default 10, “num of author names in article”
MAX_SUMMARY, default 5000, “num of chars of the summary”
MAX_SUMMARY_SENT, default 5, “num of sentences in summary”
MAX_FILE_MEMO, default 20000, “python setup.py sdist bdist_wininst upload”
memoize_articles, default True, “cache and save articles run after run”
fetch_images, default True, “set this to false if you don’t care about getting images”
follow_meta_refresh, default False, “follows a redirect url in a meta refresh html tag”
image_dimension_ration, default 16/9.0, “max ratio for height/width, we ignore if greater”
language, default ‘en’, “run newspaper.languages() to see available options.”
browser_user_agent, default ‘newspaper/%s’ % __version__
request_timeout, default 7
number_threads, default 10, “number of threads when mthreading”
verbose, default False, “turn this on when debugging”
"""

def scrap(url):   
    # Newspaper3k configuration 
    config = newspaper.Config()
    config.browser_user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'

    # Scraping
    article = newspaper.Article(url, config=config)  # , language='ko'
    try:
        logger.info("loading %s", url)
        article.download()  # request
        article.parse()  # parsing
        
#         doc_info = {
#             'title': article.title,
# #             'authors': article.authors,
#             # 'publish_date': article.publish_date,
#             'contents': article.text,
#             # 'url': url,
#             # 'crawl_at': datetime.now(),
#             # 'is_news': article.is_valid_url(),
# #             'top_image': article.top_image,
# #             'movies': article.movies
#         }

    except:
        logger.warning(f"parse_error: {url}")
        
    if article.text == '':
        logger.warning(f"title/contents is empty: {url}")

    return article.text
