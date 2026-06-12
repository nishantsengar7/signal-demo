class Rectangle:
    # keyword-only so you can't accidentally swap length and width positionally
    def __init__(self, *, length: int, width: int) -> None:
        self.length = length
        self.width = width

    def __iter__(self):
        yield {'length': self.length}
        yield {'width': self.width}

    def __repr__(self) -> str:
        return f"Rectangle(length={self.length!r}, width={self.width!r})"
