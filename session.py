import os
import aiohttp

from cmds.data_input import DataInput
from curriculum import Curriculum
from page import Page
from profile import Profile
from bs4 import BeautifulSoup


class Session:
    def __init__(self, session: aiohttp.ClientSession, cookie: str) -> None:
        self.cookie: str = cookie
        self._session: aiohttp.ClientSession = session
        self.csrf: str | None = None
        self._profile: Profile | None = None
        self._curriculum: Curriculum | None = None

    @classmethod
    async def create(cls, cookie: str):
        session = aiohttp.ClientSession(
            headers={
                'cookie': cookie,
                'origin': 'https://my.ukma.edu.ua'
            }
        )
        self = cls(session, cookie)
        await self._init_session()

        return self

    async def close(self):
        await self._session.close()

    async def _init_session(self):
        page: Page = await self._request(
            method='get',
            url='https://my.ukma.edu.ua/profile'
        )

        if page.status != 200:
            raise RuntimeError(f'init session failed, status: {page.status}')

        soup = BeautifulSoup(page.text, 'html.parser')

        await self._parse_csrf(soup)
        await self._parse_profile(soup)

    async def _parse_csrf(self, soup: BeautifulSoup):
        self.csrf = soup.find('meta', attrs={'name': 'csrf-token'}).get('content')

    async def _parse_profile(self, soup: BeautifulSoup):
        block = soup.find('dl', class_='text-center')
        if not block:
            raise RuntimeError(f'user not authorized')

        dts, dds = block.find_all('dt'), block.find_all('dd')
        data = {dt.text: dd.text for dt, dd in zip(dts, dds)}
        self._profile = Profile(
            data['Користувач'],
            data['Роль'],
            data['Етап'],
            data['Номер залікової книжки']
        )

    async def parse_curriculum(self):
        season = await DataInput.input_digit(
            message='0 - Exit\n1 - Осінь\n2 - Весна\n3 - Літо\n'
                    'Select season (enter number): ',
            digit_range=list(range(4))
        )
        if season == 0:
            os._exit(0)

        page: Page = await self._request(
            method='get',
            url='https://my.ukma.edu.ua/curriculum'
        )
        if page.status != 200:
            raise RuntimeError(f'init curriculum failed, status: {page.status}')

        self._curriculum = Curriculum(page, season)
        await self._curriculum.convert()
        await self._curriculum.create_file()

    async def refresh_curriculum(self):
        await self._curriculum.load()

    async def get_disciplines(self):
        return self._curriculum.disciplines

    async def _request(self, method: str, url: str, **kwargs) -> Page:
        async with getattr(self._session, method)(url, **kwargs) as response:
            return Page(
                status=response.status,
                text=await response.text()
            )

    async def show_profile(self):
        print(self._profile)

    async def show_curriculum(self):
        await self._curriculum.show()
