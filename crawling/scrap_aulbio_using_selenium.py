from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=options)

url = "http://aulbio.com/bbs/board.php?bo_table=d1"
driver.get(url)


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

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
articles = fetch_articles(soup)

for article in articles:
    print(f"{article['date']} | {article['views']} views | {article['name']} | {article['title']}")


driver.quit()
