from requests import get
import sys
import os
import re
from bs4 import BeautifulSoup

currentPage = 1

dirs = os.listdir()
if not dirs.__contains__('comics'):
    os.mkdir('comics')

os.chdir('comics')
while True:

    html = get(f'https://randowis.com/category/short-comics/page/{currentPage}/')

    if html.status_code != 200:
        print(f'Request returned {html.status_code}. End of comics assumed.')
        break

    soup = BeautifulSoup(html.content)

    entries = soup.find_all('img', {'class': re.compile(r'wp-image-\w+')})
    if len(entries) <= 0:
        continue

    dirName = f"Page {currentPage}"
    os.mkdir(dirName)

    for entry in entries:
        url = entry.get('src')
        fileName = entry.get('alt')
        if fileName == '':
            continue

        writePath = os.path.join(os.getcwd(), dirName, fileName)

        if not (os.path.exists(writePath) and os.path.isfile(writePath)):
            print(f'Comic Page {currentPage}/{fileName} found. Skipping...')
            continue

        with open(writePath, "wb") as f:
            print(f'Downloading {fileName}')
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

    currentPage += 1
    pass
