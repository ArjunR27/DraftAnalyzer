# Team Data Scraper for 2023-2024 Season

import requests
import csv
from bs4 import BeautifulSoup


def main():
    team_ids = ['BOS', 'BRK', 'TOR', 
               'PHI', 'NYK', 'CHI', 
               'CLE', 'DET', 'IND', 
               'MIL', 'WAS', 'ATL',
               'ORL', 'MIA', 'CHO',
               'MIN', 'OKC', 'DEN',
               'POR', 'UTA', 'LAL', 
               'LAC', 'PHO', 'GSW',
               'SAC', 'MEM', 'NOP',
               'HOU', 'SAS', 'DAL',]
    
    url = f'https://www.basketball-reference.com/teams/GSW/2024/gamelog/'
    
    response = requests.get(url)

    if response.status_code == 200:
        content = response.text
    else:
        print(f'Status code: {response.status_code}')
    
    soup = BeautifulSoup(content, 'html.parser')
    rows = soup.find_all('tr')

    if rows:
        with open('test_gsw.csv', 'w', newline='') as csvfile:
            
            field_names = ['Rk', 'G', 'Date', 
                           'H/A', 'Opp', 'W/L', 
                           'Tm', 'Opp', 'ORtg', 
                           'DRtg','Pace', 'FTr', 
                           '3PAr', 'TS%', 'TRB%', 
                           'AST%', 'STL%', 'BLK%', 
                           'eFG%', 'TOV%', 'ORB%', 
                           'FT/FGA', 'Opp_eFG%', 
                           'Opp_TOV%', 'Opp_DRB%', 'Opp_FT/FGA']
        
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writeheader()


            for row in rows:
                data_cells = row.find_all(['td', 'th'])
                row_data = [cell.text.strip() for cell in data_cells]
                print(row_data)
            


                
    
    """for team in team_ids:
        url = f'https://www.basketball-reference.com/teams/{team}/2024/gamelog/'
        response = requests.get(url)

        if response.status_code == 200:
            content = response.text
        else:
            print(f'Status code: {response.status_code}')"""


if __name__ == "__main__":
    main()


