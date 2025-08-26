import asyncio
from cmds.cmd_base import CmdBase
from dispatcher import Dispatcher


class CmdRun(CmdBase):
    def __init__(self, menu):
        super().__init__()
        self.name = 'Run'
        self._menu = menu

    async def execute(self) -> None:
        Dispatcher.running = True
        Dispatcher.cookie = self._menu.session.cookie
        Dispatcher.csrf = self._menu.session.csrf

        tasks = []

        for disc in await self._menu.session.get_disciplines():
            if disc.p1_group is None:
                continue

            task = asyncio.create_task(Dispatcher(disc).run())
            tasks.append(task)

        await asyncio.gather(*tasks)
