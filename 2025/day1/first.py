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
        self.dialUpdateValue(self.dialChange(code))
        self.zeros += self.value == 0

    def processAllChanges(self, codes: list[str]):
        for code in codes:
            self.processOneChange(code)


with open("input.txt") as f:
    data = f.read().splitlines()

dial = Dial(DIAL_INITIAL, DIAL_MAX)
dial.processAllChanges(data)
print(dial.zeros)