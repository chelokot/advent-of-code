from dataclasses import dataclass

with open("input.txt") as f:
    disk_map = f.read()

def generate_disk_partition(disk_map):
    partition = []
    adding_file = True
    file_id = 0
    for char in disk_map:
        if char == '\n':
            break
        if adding_file:
            partition += [file_id] * int(char)
            file_id += 1
        else:
            partition += ['.'] * int(char)
        adding_file = not adding_file
    return partition

partition = generate_disk_partition(disk_map)
print(partition)

empty_slots = []
files = []

start_i = 0
prev_char = partition[0]

@dataclass
class Slot:
    start: int
    length: int

@dataclass
class File:
    id: int
    start: int
    length: int
    prev_slot_id: int | None
    touches_prev_slot: bool
    touches_next_slot: bool

for i, char in enumerate(partition+['X']):
    if prev_char == char:
        continue

    if prev_char == '.':
        empty_slots.append(Slot(start = start_i, length = i - start_i))
    else:
        files.append(File(
            id = prev_char, start = start_i, length = i - start_i,
            prev_slot_id = len(empty_slots) - 1 if len(empty_slots) > 0 else None,
            touches_prev_slot = files[-1].touches_prev_slot if len(files) > 0 else len(empty_slots) > 0,
            touches_next_slot = char == '.'
        ))

    prev_char = char
    start_i = i

from collections import Counter
counter1 = Counter(partition)

for file in files[::-1]:
    for slot in empty_slots:
        if slot.length >= file.length and slot.start <= file.start:
            print(f"File {file.id} with length {file.length} fits in slot {slot.start} with length {slot.length}")
            partition[slot.start:slot.start+file.length] = [file.id] * file.length
            partition[file.start:file.start+file.length] = ['.'] * file.length
            slot.start += file.length
            slot.length -= file.length

            # If touches both prev and next slot, merge them
            if file.touches_prev_slot and file.touches_next_slot:
                empty_slots[file.prev_slot_id].length += file.length + empty_slots[file.prev_slot_id + 1].length
                # Delete next slot
                del empty_slots[file.prev_slot_id + 1]
                for _file in files:
                    if _file.prev_slot_id and _file.prev_slot_id > file.prev_slot_id:
                        _file.prev_slot_id -= 1
            # If touches only prev slot, extend it
            elif file.touches_prev_slot:
                empty_slots[file.prev_slot_id].length += file.length
            # If touches only next slot, extend it
            elif file.touches_next_slot:
                empty_slots[file.prev_slot_id + 1].start -= file.length
                empty_slots[file.prev_slot_id + 1].length += file.length
            # Else, we have to create a new slot
            else:
                empty_slots.insert(file.prev_slot_id + 1, Slot(start = file.start, length = file.length))
                for _file in files:
                    if _file.prev_slot_id and _file.prev_slot_id > file.prev_slot_id:
                        _file.prev_slot_id += 1
            break

print(partition)

counter2 = Counter(partition)
for key in counter1:
    if counter1[key] != counter2[key]:
        print(f"Error: {key} count changed from {counter1[key]} to {counter2[key]}")

def checksum(partition):
    return sum(i*int(c) for i, c in enumerate(partition) if c != '.')
print(checksum(partition))
