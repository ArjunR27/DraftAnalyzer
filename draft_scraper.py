# Draft Data Scraper for 2023 Draft

import requests
import csv
import time
from bs4 import BeautifulSoup

def main():
    for year in range(2013, 2023):
        url = f"https://www.basketball-reference.com/draft/NBA_{year}.html"

        response = requests.get(url)

        if response.status_code == 200:
            content = response.text
        else:
            print(f'Status code: {response.status_code}')

        
        soup = BeautifulSoup(content, 'html.parser')
        tds = soup.find_all('td', attrs={'data-stat': True})

        player_row = {}
        columns = set()
        columns.add('year')

        player_data = []
        header_written = False
        for td in tds:
            # print(td['data-stat'], td.text.strip())
            player_row['year'] = year
            data_stat = td['data-stat']
            value = td.text.strip()
            columns.add(data_stat)

            if data_stat == 'vorp' and player_row:
                player_data.append(player_row)
                player_row = {}
            
            player_row[data_stat] = value
        
        if player_row:
            player_data.append(player_row)
        
        with open('draft_stats.csv', 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns)
            if not header_written:
                writer.writeheader()
                header_written = True
            
            for row in player_data:
                if len(row) > 1:
                    writer.writerow(row)
        time.sleep(3)


if __name__ == "__main__":
    main()
