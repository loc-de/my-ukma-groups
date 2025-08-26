from cmds.cmd_base import CmdBase
import os


class CmdExit(CmdBase):
    def __init__(self):
        super().__init__()
        self.name = 'Exit'

    async def execute(self) -> None:
        os._exit(1)
