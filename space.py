import enum
from enum import auto


class Piece(enum.Enum):
    WHITE = auto()
    BLACK = auto()
    EMPTY = auto()


class Space:
    def __init__(self, space_id: str, piece: Piece = Piece.EMPTY):
        self._space_id = space_id
        self._piece = piece

    @property
    def space_id(self):
        return self._space_id

    @property
    def piece(self):
        return self._piece.name

    @piece.setter
    def piece(self, piece: Piece):
        self._piece = piece

    def __str__(self) -> str:
        return f"Space ID: {self.space_id}\n" \
               f"Piece: {self.piece}\n"
