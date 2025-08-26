from cmds.cmd_base import CmdBase


class CmdRefresh(CmdBase):
    def __init__(self, menu):
        super().__init__()
        self.name = 'Refresh'
        self._menu = menu

    async def execute(self) -> None:
        await self._menu.session.refresh_curriculum()
        await self._menu.session.show_curriculum()
        print()
