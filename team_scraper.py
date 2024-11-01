# Team Data Scraper for 2023-2024 Season

import requests
import csv
import time
from bs4 import BeautifulSoup


def main():
    team_ids = ['BOS', 'BRK', 'TOR', 'PHI', 'NYK', 'CHI', 'CLE', 'DET', 'IND', 'MIL', 'WAS', 'ATL', 'ORL', 'MIA', 'CHO', 'MIN', 'OKC',
                'DEN', 'POR', 'UTA', 'LAL', 'LAC', 'PHO', 'GSW', 'SAC', 'MEM', 'NOP', 'HOU', 'SAS', 'DAL']
    header_written = False

    ignore_columns = {'opp_efg_pct', 'opp_tov_pct', 'opp_id', 'opp_pts', 'opp_ft_rate'}
    for year in range(2014, 2023):
        for team in team_ids: 
            url = f'https://www.basketball-reference.com/teams/{team}/{year}/gamelog-advanced/'
            
            response = requests.get(url)

            if response.status_code == 200:
                content = response.text
            else:
                print(f'Status code: {response.status_code}')
            
            soup = BeautifulSoup(content, 'html.parser')
            tds = soup.find_all('td', attrs={'data-stat': True})
            
            game_data = []
            columns = set()
            columns.add('team_id')

            game_row = {}
            for td in tds:
                game_row['team_id'] = team
                data_stat = td['data-stat']
                if data_stat in ignore_columns:
                    continue
                value = td.text.strip()

                columns.add(data_stat)

                if data_stat == 'game_season' and game_row:
                    game_data.append(game_row)
                    game_row = {}
                    
                game_row[data_stat] = value

            if game_row:
                game_data.append(game_row)
            
            with open('game_stats.csv', 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=columns)
                if not header_written:
                    writer.writeheader()
                    header_written = True

                for row in game_data:
                    if len(row) > 1:
                        writer.writerow(row)
            
            # Adding time delay so basketball reference doesn't block the program
            time.sleep(3)


if __name__ == "__main__":
    main()