class Profile:
    def __init__(self, name: str, role: str, stage: str, book_num: str):
        self._name = name
        self._role = role
        self._stage = stage
        self._book_num = book_num

    def __str__(self):
        return (f'    Профіль\n'
                f'Користувач: {self._name}\n'
                f'Роль: {self._role}\n'
                f'Етап: {self._stage}\n'
                f'Номер залікової книжки: {self._book_num}')
