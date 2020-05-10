from requests import get
import sys
import os
import re
import argparse
from bs4 import BeautifulSoup


def get_image_elements(current_page):
    html = get(f'https://randowis.com/category/short-comics/page/{current_page}/')

    if html.status_code != 200:
        print(f'Request returned {html.status_code}. End of comics assumed.')
        return None
    return BeautifulSoup(html.content).find_all('img', {'class': re.compile(r'wp-image-\w+')})


def create_comics_dir():
    dirs = os.listdir()
    if not dirs.__contains__('comics'):
        os.mkdir('comics')
    os.chdir('comics')


def download_file(file_name, url):
    with open(file_name, "wb") as f:
        print(f'Downloading {file_name}')
        response = get(url, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None:
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
                sys.stdout.flush()


def fetch_comics(keep_page_structure):
    current_page = 1

    while True:

        entries = get_image_elements(current_page)
        if entries is None or len(entries) <= 0:
            current_page += 1
            continue

        dir_name = f"Page {current_page}" if keep_page_structure else ''

        if dir_name != '' and not os.path.exists(dir_name):
            os.mkdir(dir_name)

        for entry in entries:
            url = entry.get('src')
            file_name = entry.get('alt')
            if file_name == '':
                continue

            write_path = os.path.join(os.getcwd(), dir_name, file_name)

            if os.path.exists(write_path) and os.path.isfile(write_path):
                print(f'Comic Page {current_page}/{file_name} found. Skipping...')
                continue

            download_file(write_path, url)

        current_page += 1
        pass


def get_args():
    ap = argparse.ArgumentParser()

    ap.add_argument('-f', '--first', help='Gets the first comic on the first page', action='store_true')
    ap.add_argument('-ks', '--keep-page-structure', help="Comics will be separated by pages",
                    action='store_true')

    return vars(ap.parse_args())


if __name__ == '__main__':
    args = get_args()
    create_comics_dir()
    fetch_comics(args['keep_page_structure'])
