from pydantic import BaseModel


class Discipline(BaseModel):
    id_: int
    name: str
    c_group: int | None
    p1_group: int | None = None
    p2_group: int | None = None
    number: int

    def as_row(self) -> list[str]:
        return [
            str(self.id_),
            str(self.c_group) if self.c_group else "-",
            str(self.p1_group) if self.p1_group else "-",
            str(self.p2_group) if self.p2_group else "-",
            self.name
        ]
