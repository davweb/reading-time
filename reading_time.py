"""Return the reading time for a URL"""

import argparse
import math
from typing import Callable
from fake_useragent import UserAgent
from html2text import html2text
from readabilipy import simple_json_from_html_string
from readability import Document
import requests

CHROME = UserAgent().chrome


def download_page(url: str) -> str:
    """Download the specified URL"""

    response = requests.get(url, headers={'User-Agent': CHROME}, timeout=60)

    # pylint: disable=no-member
    if response.status_code != requests.codes.ok:
        raise RuntimeError(f'Request for {url} failed with code {response.status_code}')

    return response.text


def article_content(content: str) -> str:
    """Parse an HTML page and extract content as text"""

    doc = Document(content)
    return html2text(doc.summary())


def alternative_article_content(content: str) -> str:
    """Parse an HTML page and extract content as text use an alternate method"""

    article = simple_json_from_html_string(content)
    return ' '.join(item['text'] for item in iter(article['plain_text']))


def whole_page_content(content: str) -> str:
    """Return a whole HTML page as text"""
    return html2text(content)


def reading_time(url: str, processor: Callable[[str], str], words_per_minute: int) -> int:
    """Return the reading time for a URL in minutes"""

    content = download_page(url)
    text = processor(content)
    word_count = len(text.split())
    return math.ceil(word_count / words_per_minute)


def main() -> None:
    """Entrypoint method"""

    parser = argparse.ArgumentParser('Calculate reading time for URL')
    parser.add_argument('-s', '--reading-speed',
                        help='Reading speed in words per minute',
                        type=int, default=200, metavar='<wpm>')
    parser.add_argument('urls', metavar='<url>', nargs='+',
                        help='The urls to calculate the reading speed for')

    parsers = parser.add_mutually_exclusive_group()
    parsers.add_argument('-a', '--alternate', action='store_true',
                         help='Use alternative method to extract article content')
    parsers.add_argument('-w', '--whole-page', action='store_true',
                         help='Calculate reading time based on the whole page')

    args = parser.parse_args()

    if args.whole_page:
        processor = whole_page_content
    elif args.alternate:
        processor = alternative_article_content
    else:
        processor = article_content

    for url in args.urls:
        reading_time_minutes = reading_time(url, processor, args.reading_speed)
        print(f'\n{url}\n{reading_time_minutes} minutes reading time.')


if __name__ == "__main__":
    main()
