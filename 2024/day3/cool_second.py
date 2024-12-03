import re
with open("input.txt") as f:
    data = f.read()

pattern = r"(?:^|do\(\)).*?(?:mul\((\d{1,3}),(\d{1,3})\).*?)*?(?:$|don't\(\))"
print(re.findall(pattern, data, re.DOTALL))
print(sum(map(lambda I: int(I[0]) * int(I[1]),re.findall(pattern, data, re.DOTALL))))
