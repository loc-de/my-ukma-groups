import asyncio
import aiohttp
from discipline import Discipline
from page import Page


class Dispatcher:
    running: bool = False
    cookie: str = ''
    csrf: str = ''

    def __init__(self, discipline: Discipline):
        self._disc = discipline
        self._session = aiohttp.ClientSession(
            headers={
                'cookie': Dispatcher.cookie,
                'origin': 'https://my.ukma.edu.ua',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36'
            }
        )

    async def run(self):
        while Dispatcher.running:
            if await self._send():
                break

            await asyncio.sleep(3)

        await self._session.close()

    async def _send(self) -> bool:
        page: Page = await self._request(
            method='post',
            url='https://my.ukma.edu.ua/curriculum/groups',
            data={
                '_csrf': Dispatcher.csrf,
                f'course_group[{self._disc.number}]': f'{self._disc.p1_group}'
            }
        )
        return page.status == 200

    async def _request(self, method: str, url: str, **kwargs) -> Page:
        async with getattr(self._session, method)(url, **kwargs) as response:
            return Page(
                status=response.status,
                text=await response.text()
            )
