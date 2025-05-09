import requests
from bs4 import BeautifulSoup

url = 'http://aulbio.com/bbs/board.php?bo_table=d1&ckattempt=1'

headers = {
    'authority': 'www.amazon.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-dest': 'document',
    'accept-language': '*',
}

def get_page():
    response = requests.get(url, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
    return response

def fetch_articles(soup):
    articles = []

    rows = soup.select('tbody > tr')
    for row in rows:
        title_tag = row.select_one('.td_subject a')
        name_tag = row.select_one('.td_name.sv_use .sv_member')
        num_tag = row.select_one('.td_num')
        date_tag = row.select_one('.td_datetime')

        if title_tag and name_tag and num_tag and date_tag:
            article = {
                'title': title_tag.text.strip(),
                'name': name_tag.text.strip(),
                'views': num_tag.text.strip(),
                'date': date_tag.text.strip()
            }
            articles.append(article)

    return articles

page = get_page()
soup = BeautifulSoup(page.content, 'html.parser')
articles = fetch_articles(soup)

for article in articles:
    print(f"{article['date']} | {article['views']} views | {article['name']} | {article['title']}")

