class CmdBase:
    def __init__(self):
        self.name: str = ''

    async def execute(self) -> None:
        print(f'{self.name}:')
