import asyncio
import os

from cmds.cmd_base import CmdBase
from cmds.data_input import DataInput

from cmds.cmd_run import CmdRun
from cmds.cmd_refresh import CmdRefresh
from cmds.cmd_exit import CmdExit

from session import Session


class Menu:
    def __init__(self, session: Session):
        self._menu: list[CmdBase] = [
            CmdExit(),
            CmdRefresh(self),
            CmdRun(self)
        ]
        self.session: Session = session

    @classmethod
    async def create(cls):
        cookie = input("Enter cookie line: ")
        print()

        session = await Session.create(cookie)
        await session.show_profile()
        print()

        await session.parse_curriculum()
        await session.show_curriculum()
        print()

        return cls(session)

        # await session.profile.curriculum.show(1)

    async def show_main_menu(self) -> None:
        print('    Menu:')

        for inx, cmd in enumerate(self._menu):
            print(f"{inx} - {cmd.name}")

        print('')

    async def execute(self) -> None:
        key: int = await DataInput.input_digit(
            message='Select command (enter number): ',
            digit_range=list(range(len(self._menu)))
        )

        await self._menu[key].execute()

    @staticmethod
    async def _show_menu(cmds_list: list[CmdBase]) -> None:
        print('Commands list: \n0 - Back')
        for inx, obj in enumerate(cmds_list):
            print(f'{inx + 1} - {obj.name}')

        print('')
