import os
import urllib2
import traceback

_BASE_URL_FILEPATH = os.path.join(os.path.dirname(__file__), "base_url.txt")
_BASE_URL_URL      = "http://tralhas.xyz/geturl/url.txt"
_BASE_URL_DEFAULT  = "http://ratotv.top/"

def get_base_url(refresh=False):
    base_url = None
    if refresh:
        base_url = get_base_url_from_url()
        if base_url is None:
            base_url = get_base_url_from_file()
        else:
            write_base_url_to_file(base_url)
    else:
        base_url = get_base_url_from_file()
        if base_url is None:
            base_url = get_base_url_from_url()
            if base_url is not None:
                write_base_url_to_file(base_url)
    if base_url is None:
        base_url = _BASE_URL_DEFAULT
    if not base_url.endswith("/"):
        base_url + "/"
    return base_url


def write_base_url_to_file(base_url):
    try:
        f = open(_BASE_URL_FILEPATH, "w")
        f.write(base_url)
        f.close()
    except:
        traceback.print_exc()

def get_base_url_from_file():
    try:
        f = open(_BASE_URL_FILEPATH, "r")
        base_url = f.read()
        f.close()
    except:
        traceback.print_exc()
        return
    return base_url


def get_base_url_from_url():
    request = urllib2.Request(_BASE_URL_URL)
    request.add_header("User-Agent", "Wget/1.15 (linux-gnu)")
    try:
        response =  urllib2.urlopen(request)
        base_url = response.read()
        response.close()
    except:
        traceback.print_exc()
        return
    return base_url


if __name__ == "__main__":
    print get_base_url(True)

