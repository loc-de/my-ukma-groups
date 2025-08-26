import asyncio
from menu import Menu


async def main():
    menu = await Menu.create()

    while True:
        await menu.show_main_menu()
        await menu.execute()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except RuntimeError as e:
        print(str(e))
