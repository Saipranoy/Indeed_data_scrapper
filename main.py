import requests
from bs4 import BeautifulSoup
import pandas as pd


def extract(page):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.62 Safari/537.36'}
    url = f'https://uk.indeed.com/jobs?q=data%20analyst&l=London,%20Greater%20London&start={page}&vjk=47eb76f7be77a582&advn=3158115976709409'
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup


def transform(soup):
    divs = soup.find_all('div', class_ = 'cardOutline')
    for item in divs:
        title = item.find('a').text
        company = item.find('span', class_ = 'companyName').text
        try:
            salary = item.find('div', class_='metadata salary-snippet-container').text
        except:
            salary = ''
        summary = item.find('div', class_ = 'job-snippet').text.replace('\n','')

        job = {
            'title': title,
            'company':company,
            'salary':salary,
            'summary':summary
        }
        joblist.append(job)
    return


joblist = []
for i in range(0,40,10):
    c = extract(0)
    transform(c)
df = pd.DataFrame(joblist)
print(df.head())
df.to_csv('jobs.csv')