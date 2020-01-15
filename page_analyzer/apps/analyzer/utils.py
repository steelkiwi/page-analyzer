import requests
import re
from urllib.request import urlparse, urljoin


def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_links(soup, url):
    links = []
    internal_links = []
    external_links = []
    domain_name = urlparse(url).netloc
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # href empty tag
            continue
        # join the URL if it's relative (not absolute link)
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        # remove URL GET parameters, URL fragments, etc.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not is_valid_url(href):
            # not a valid URL
            continue
        if href in internal_links:
            # already in the set
            continue
        if domain_name not in href:
            # external link
            if href not in external_links:
                external_links.append(href)
            continue
        links.append(href)
        internal_links.append(href)
    return {'links': links, 'internal': internal_links, 'external': external_links}


def links_count_inaccessible(links):
    inaccessible_count = 0
    for link in links:
        if not link_is_accessible(link):
            inaccessible_count += 1
    return inaccessible_count


def link_is_accessible(url):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == requests.codes.ok:
            return True
        else:
            return False
    except requests.Timeout:
        return False
    except requests.TooManyRedirects:
        return False
    except requests.RequestException:
        return False
