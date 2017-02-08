import random


def read_file(filename):
    """
    (str) -> (data)
    """
    with open(filename, encoding="utf-8") as data:
        datas = [line.replace("\n", "") for line in data if line]
    return datas

#print(read_file("field_txt.txt"))


def has_ship(data, coordinates):
    """
    (data, tuple) -> (bool)
    """
    if data[coordinates[1] - 1][ord(coordinates[0]) - 65] == " ":
        return False
    else:
        return True


def ship_size(data, coordinates):
    """
    (data, tuple) -> (tuple)
    """
    coordinates_list = [coordinates]
    coordinates = (ord(coordinates[0]) - 65, coordinates[1] - 1)
    length = 1
    horisontal = False
    for i in range(1, 4):
        if coordinates[0] - i >= 0:
            if data[coordinates[1]][coordinates[0] - i] != " ":
                length += 1
                coordinates_list.append((chr(coordinates[0] + 65), coordinates[1] - i + 1))
                horisontal = True
            else:
                break
        else:
            break
    if length < 4:
        for i in range(1, 4):
            if coordinates[0] + i <= 9:
                if data[coordinates[1]][coordinates[0] + i] != " ":
                    length += 1
                    coordinates_list.append((chr(coordinates[0] + 65), coordinates[1] + i + 1))
                    horisontal = True
                else:
                    break
            else:
                break
    if not horisontal:
        for i in range(1, 4):
            if coordinates[1] - i >= 0:
                if data[coordinates[1] - i][coordinates[0]] != " ":
                    length += 1
                    coordinates_list.append((chr(coordinates[0] - i + 65), coordinates[1] + 1))
                else:
                    break
            else:
                break
        for i in range(1, 4):
            if coordinates[1] + i <= 9:
                if data[coordinates[1] + i][coordinates[0]] != " ":
                    length += 1
                    coordinates_list.append((chr(coordinates[0] + i + 65), coordinates[1] + 1))
                else:
                    break
            else:
                break
    return length, coordinates_list


def is_valid(data):
    """
    (data) -> (bool)
    """
    ships = {1: 0, 2: 0, 3: 0, 4: 0}
    coordinates_set = set()
    for line in range(1, 11):
        for symbol in range(65, 75):
            if (chr(symbol), line) in coordinates_set:
                continue
            if data[line - 1][symbol - 65] != " ":
                size_result = ship_size(data, (chr(symbol), line))
                coordinates_set.update(size_result[1])
                ships[size_result[0]] += 1
    if ships[1] > 3 and ships[2] > 2 and ships[3] > 1 and ships[4] > 0:
        return True
    else:
        return False


def field_to_str(data):
    """
    (data) -> (str)
    """
    data_string = ""
    for line in data:
        data_string += line + '\n'
    return data_string


def ship_outline(data):
    """
    (set) -> (set)
    """
    outline_set = set()
    for coordinate in data:
        for i in range(-1, 2):
            if -1 < coordinate[0] + i < 10:
                for j in range(-1, 2):
                    if j == 0 and i == 0:
                        continue
                    if -1 < coordinate[1] + j < 10:
                        outline_set.add((coordinate[0] + i, coordinate[1] + j))
    return outline_set


def generate_field():
    """
    () -> (data)
    """
    field_set = set()
    for i in range(4):
        for j in range(i + 1):
            while True:
                single_ship = (random.randrange(0, 7 + i), random.randrange(0, 7 + i))
                horisontal = random.choice([True, False])
                data = {single_ship}
                if horisontal:
                    for l in range(1, 4 - i):
                        data.add((single_ship[0] + l, single_ship[1]))
                else:
                    for l in range(1, 4 - i):
                        data.add((single_ship[0], single_ship[1] + l))
                if ship_outline(data) & field_set == set():
                    field_set |= data
                    break
    data_result = []
    for y in range(1, 11):
        line = ""
        for x in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']:
            if (ord(x) - 65, y - 1) in field_set:
                line += "*"
            else:
                line += " "
        data_result.append(line)
    if is_valid(data_result):
        return data_result
    else:
        return generate_field()
