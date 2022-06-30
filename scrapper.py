# Quizlet Flash Card Scraper

import bs4
import re
import requests
import sys
U = 'https://quizlet.com/'


# URL = sys.argv[1]
def writetofile(c):
    print("Content Found\nWriting to file")
    with open('out.txt', 'a') as f:
        f.write(c)
    print('Done')



def main():
    for x in range(12002,12005):
        URL = U+str(x)+'/ '
        print(x)
        # Var declarations
        cards, a, counter, cut = "", False, 0, False


        # Header config from Dean Ambros on Stack Overflow
        # https://stackoverflow.com/questions/63910238/how-to-get-data-from-quizlet-without-getting-blocked-for-web-scraping
        HEADERS = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'cookie': 'yourcookie',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 12239.92.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.136 Safari/537.36',
        }

        # Gets bs4 soup object for URL
        raw_site_page = requests.get(URL, headers=HEADERS)
        raw_site_page.raise_for_status()
        soup = bs4.BeautifulSoup(raw_site_page.text, 'html.parser')

        # Appends all questions and answers to cards
        for p in soup.find_all(class_='SetPageTerm-sideContent'):
            if a:
                cards += f'\tA{counter + 1}) {p.text}\n'
                a = False
                counter += 1
                q = re.sub(r'(?<=\.)TrueFalse', '',
                            re.sub(r'(?<=\?)[\W\w\.]+', '', p.text))  # Particular to my example
                q = p.text
                cards += f'Q{counter + 1}) {q}\n'
                a = True

        # Writes cards to text file if worked
        if cards == "":
            print("No content found")
        else:
            writetofile(cards)

if __name__ == '__main__':
    main()
