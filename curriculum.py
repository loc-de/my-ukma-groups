import json
from bs4 import BeautifulSoup

from page import Page
from discipline import Discipline


class Curriculum:
    def __init__(self, page: Page, season: int):
        self._page = page
        self._season = season
        self._season_name = ['осінь', 'весна', 'літо'][season - 1]

        self._years = ''
        self._disciplines: dict[str, Discipline] = {}

    async def convert(self):
        soup = BeautifulSoup(self._page.text, 'html.parser')

        self._years = soup.find('small').get_text(strip=True).replace('на ', '')

        counter = 1
        for row in soup.select("tbody tr"):
            name_cell = row.select_one("td.text-left.cell-name")
            if not name_cell:
                continue

            number_span = name_cell.find("span", class_="label label-default hidden-print")
            group_span = name_cell.find("span", class_="label label-success hidden-print")
            number = int(number_span.get_text(strip=True)) if number_span else None
            group = int(group_span.get_text(strip=True).replace(' група', '')) if group_span else None

            link = name_cell.find("a")
            name = link.get_text(strip=True) if link else None

            season_cells = row.select("td.cell-season")
            if len(season_cells) != 3:
                continue

            if season_cells[self._season - 1].get_text(strip=True) != '':
                discipline = Discipline(
                    id_=counter,
                    name=name,
                    c_group=group,
                    number=number
                )
                self._disciplines[name] = discipline
                counter += 1

    async def create_file(self):
        priorities = {
            'disciplines': [
                {
                    'name': d.name,
                    'p1_group': None,
                    'p2_group': None
                } for d in self._disciplines.values()
            ]
        }

        with open('priorities.json', 'w', encoding='utf-8') as file:
            json.dump(priorities, file, ensure_ascii=False, indent=4)

    async def load(self):
        with open('priorities.json', 'r', encoding='utf-8') as file:
            priorities = json.load(file)

        disciplines = priorities.get('disciplines')
        if disciplines is None:
            return

        for d_data in disciplines:
            if 'p1_group' not in d_data or 'p2_group' not in d_data or 'name' not in d_data:
                continue

            d = self._disciplines.get(d_data['name'])
            if d is None:
                continue

            d.p1_group = d_data['p1_group']
            d.p2_group = d_data['p2_group']

    async def show(self):
        headers = ['Номер', "Поточна", "Пріор.1", "Пріор.2", "Назва"]
        col_widths = [len(h) for h in headers]
        for d in self._disciplines.values():
            for i, value in enumerate(d.as_row()):
                col_widths[i] = max(col_widths[i], len(value))

        header_row = "   ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
        print(f'    ІНП на {self._season_name} {self._years}\n{header_row}')

        for inx, d in enumerate(self._disciplines.values(), start=1):
            row = "   ".join(val.ljust(col_widths[i]) for i, val in enumerate(d.as_row()))
            print(row)

    @property
    def disciplines(self):
        return self._disciplines.values()
