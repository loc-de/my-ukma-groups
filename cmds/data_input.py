import asyncio


class DataInput:
    @staticmethod
    async def input(message: str) -> str:
        input_str = await DataInput._get_input(message)
        print('')
        return input_str

    @staticmethod
    async def input_float(message: str) -> float:
        while True:
            user_input: str = (await DataInput._get_input(message)).strip()

            try:
                if user_input.strip() == '/':
                    return float('-inf')
                result = float(user_input.strip().replace(',', '.'))
                print('')
                return result
            except ValueError:
                print('Invalid input. Please try again.\n')

    @staticmethod
    async def input_digit(message: str, digit_range: list[int]) -> int:
        while True:
            user_input: str = (await DataInput._get_input(message)).strip()

            if user_input.strip() == '/':
                return 0

            if await DataInput._is_range_digit(user_input, digit_range):
                print('')
                return int(user_input)

            print('Invalid input. Please try again.\n')

    @staticmethod
    async def _is_range_digit(input_str: str, digit_range: list[int]) -> bool:
        if input_str.isdigit() and int(input_str) in digit_range:
            return True
        return False

    @staticmethod
    async def _get_input(prompt: str = '') -> str:
        return await asyncio.to_thread(input, prompt)
