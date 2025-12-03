with open("input.txt") as f:
    banks = f.read().splitlines()

def findBestNDigitSubsuqeunce(sequence: str, n: int) -> list[str]:
    best = max(sequence[: len(sequence) - (n-1)])
    return [best] + (
        findBestNDigitSubsuqeunce(sequence[sequence.find(best) + 1 :], n - 1)
        if n > 1 else []
    )

def findBiggestNNumber(bank: str, n: int) -> int:
    return int("".join(findBestNDigitSubsuqeunce(bank, n)))

print(sum(findBiggestNNumber(bank, 12) for bank in banks))
