DIAL_MAX = 99
DIAL_INITIAL = 50

class Dial:
    def __init__(self, value, max):
        self.value = value
        self.length = max + 1
        self.zeros = 0

    def dialUpdateValue(self, change: int):
        self.value = ((self.value + change) % self.length + self.length) % self.length

    def dialChange(self, code: str) -> int:
        return int(code[1:]) * (-1 if code[0] == "L" else 1)

    def processOneChange(self, code: str):
        old_value = self.value
        change = self.dialChange(code)
        value = self.value + self.dialChange(code)
        zeros = abs(value) // self.length + (1 if value < 0 and old_value != 0 else 0)
        zeros += 1 if value == 0 and change != 0 else 0
        self.zeros += zeros
        self.dialUpdateValue(change)

    def processAllChanges(self, codes: list[str]):
        for code in codes:
            self.processOneChange(code)


with open("input.txt") as f:
    data = f.read().splitlines()

dial = Dial(DIAL_INITIAL, DIAL_MAX)
dial.processAllChanges(data)
print(dial.zeros)