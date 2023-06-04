'''
    * We are scraping medium.com with the top 5 python publication
    * No of days will be generated by this code snippet, from 1 to 365 list of numbers will be generated based on the given_no_of_days
        ==> random_no_of_days = random.sample([i for i in range(1,365)],int(given_no_of_days))
    * get_day_month ==> will get the month and date of that month
    * get_claps_count ==> will get the claps count if its not available will return 0
    * Maximum 50 artciles can be fetched per publication minimum we can modify the count
    * Maximum 50 has been set to avoid web scrapping attack
'''

import requests
import sys
import logging as log
import random
from bs4 import BeautifulSoup
import datetime
from prettytable import PrettyTable
from email_service import email_sender
import utils


log.basicConfig(level=log.INFO,format='%(levelname)s:%(message)s')

urls = {
    'Towards Data Science': 'https://towardsdatascience.com/archive/{0}/{1:02d}/{2:02d}',
    'Better Programming Hub': 'https://betterprogramming.pub/archive/{0}/{1:02d}/{2:02d}',
    'Python In Plain English': 'https://python.plainenglish.io/archive/{0}/{1:02d}/{2:02d}',
    'Pragmatic Programmer': 'https://medium.com/pragmatic-programmers/archive/{0}/{1:02d}/{2:02d}',
    # 'The Startup' : 'https://medium.com/swlh/archive/{0}/{1:02d}/{2:02d}'
}

# modify the year you want
year : int = 2022
# Number of articles you want for per publication
no_of_artcile : int = 2
# Number of days 
no_of_days : int = 1
# recipients email
recipient_email : str = 'dineshshazam@gmail.com' 


@utils.exception_handler
def main():
    tabular_fields = ['Publication','Title','Title Description','Article URL','DATE', 'Claps', 'Reading Time']
    tabular_table = PrettyTable()
    tabular_table.field_names = tabular_fields


    if no_of_artcile > 50:
        log.error(f'Number of article should not be above 54, given value {no_of_artcile}')
        sys.exit()

    #* random list of no will be given from 1 to 365 , given_no_of_days indicates how many days we want
    random_no_of_days = random.sample([i for i in range(1,365)],int(no_of_days))
    #* loop through random_no_of_days
    for d in random_no_of_days:     
        #* get the month and date from random_no_of_days 
        month,day = utils.get_day_month(d)
        date = '{0}-{1:02d}-{2:02d}'.format(year,month,day)
        log.info(f'DATE : {date}')

        # if the date is future date skiping the iteration 
        current_date = datetime.date.today()
        given_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        if given_date > current_date:
            log.info(f'Skipping Future date {date}')
            continue

        #* loop through url and make request
        for publication,url in urls.items():
            response = requests.get(url.format(year,month,day),allow_redirects=True)
            if not response.url.startswith(url.format(year,month,day)):
                continue
            page = response.content
            soup = BeautifulSoup(page,'html.parser')
            articles = soup.find_all('div',
                                     class_='postArticle postArticle--short js-postArticle js-trackPostPresentation js-trackPostScrolls')

            for index,article in enumerate(articles):
                if index >= no_of_artcile:
                    break
                title_tag = article.find('h3', class_='graf--title')
                title_desc_tag = article.find('h4', class_='graf--subtitle')
                
                #* if title is not available skipping the iteration
                if title_tag is None or title_desc_tag is None:
                    continue

                article_title = title_tag.string
                article_title_desc = title_desc_tag.text
                article_url = article.find_all('a')[3]['href'].split('?')[0] 
                claps_tag = article.find('button',class_='button button--chromeless u-baseColor--buttonNormal js-multirecommendCountButton u-disablePointerEvents')
                article_claps = utils.get_claps_count('' if claps_tag is None else claps_tag.text)
                article_claps_text = f'{article_claps} claps'
                article_reading_time = article.find('span',class_='readingTime')
                article_reading_time = 0 if article_reading_time is None else article_reading_time['title']
        
                tabular_table.add_row([publication,article_title,article_title_desc,article_url,date,article_claps_text,article_reading_time]) 
        
  
    email_sender.email_template_obj(tabular_table.get_html_string(),recipient_email)
 

main()