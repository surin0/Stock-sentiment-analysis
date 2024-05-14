from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
from datetime import date
from matplotlib import pyplot as plt
from datetime import datetime

today = datetime.now()
print(today)
formatted_date = today.strftime('%Y-%m-%d')

finviz_url = "https://finviz.com/quote.ashx?t="

tickers = ['AMZN', 'GOOG', 'AMD']

news_tables = {}

for ticker in tickers:
    url = finviz_url +ticker
    
    req = Request(url=url, headers={'user-agent': 'my-app'})
    response = urlopen(req)
    
    html =BeautifulSoup(response, 'html')
    
    news_table = html.find(id='news-table')
    news_tables[ticker] = news_table
    
    
parsed_data = []

for ticker, news_table in news_tables.items():
    for row in news_table.findAll('tr'):
        title = row.a.text
        
        date_data = row.td.text.strip().split(' ')
        
        
        if len(date_data) == 1:
            time = date_data[0].strip() 
        else:
            
            date = date_data[0]
            if "Today" in date_data[0]:
                date = str(formatted_date)
            else:
                parsed_date = datetime.strptime(date, "%b-%d-%y")
                date = parsed_date.strftime("%Y-%m-%d")
            time = date_data[1].strip() 
        parsed_data.append([ticker, date, title])




df = pd.DataFrame(parsed_data, columns=['ticker', 'date', 'title'])
vader = SentimentIntensityAnalyzer()
print(df['date'])


f = lambda title: vader.polarity_scores(title)['compound']
df['compound'] = df['title'].apply(f)
df['date'] = pd.to_datetime(df.date).dt.date



plt.figure(figsize=(10,6))

mean_df = df.groupby(['ticker', 'date'])['compound'].mean().unstack()

mean_df = mean_df.transpose()
mean_df.plot(kind='bar')
plt.show()