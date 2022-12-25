class File:
    def __init__(self, name: str, size=0) -> None:
        self.name = name
        self.size = size
        self.is_created = False

    def __str__(self) -> str:
        return "{} ({}, size={})".format(self.name, "file", self.size)

    def __repr__(self) -> str:
        # Instead of printing out <class 'str'>, it prints out as follows
        return "File '{}'".format(self.name)
