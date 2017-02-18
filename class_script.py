class Game:
    def __init__(self):
        self.__fields = list()
        self.__players = list()
        self.__curent_player = 0
    def play_game(self):
        input("Please press enter to start...")
        for i in range(2):
            self.add_player()
            input("Press enter to see your field...")
            print(self.field_with_ships(self.__curent_player))
            input("Press enter")
            print(10 * "\n")
            self.__curent_player += 1
        while True:
            for i, k in ((1, 2), (2, 1)):
                result_shot = True
                while result_shot == True:
                    print("Player {0} is playing".format(i))
                    input("Press enter to see ...")
                    print("Enemy's field\n{0}".format(self.field_without_ships(k - 1)))
                    print("Your field\n{0}".format(self.field_with_ships(i - 1)))
                    result_shot = self.shoot_at(k - 1, self.__players[0].read_position())
                    while result_shot == None:
                        print("You were shooting this field, try again")
                        print("Enemy's field\n{0}".format(self.field_without_ships(k - 1)))
                        result_shot = self.shoot_at(k - 1, self.__players[0].read_position())
                    if result_shot == True:
                        print("N1 shot")
                        if not self.__fields[k - 1].has_ships():
                            return "Player {0} has won".format(i)
                    else:
                        print("Try next time...")




    def add_player(self):
        print("Please enter the name of player {0}".format(self.__curent_player + 1))
        self.__players.append(Player(input()))
        self.__fields.append(Field())

    def shoot_at(self, index, tuple_):
        return self.__fields[index].shoot_at(tuple_)

    def field_with_ships(self, index):
        return self.__fields[index].field_with_ships()

    def field_without_ships(self, index):
        return self.__fields[index].field_without_ships()


class Player:
    def __init__(self, name="Player"):
        self.__name = name

    @staticmethod
    def read_position():
        input_ = input("Type coordinate of type C1").strip()
        while len(input_) != 2:
            input_ = input("Type C1 or B2 or A1").strip()
        x, y = input_[0], int(input_[1])
        return ord(x.upper()) - 65, y - 1
#a = Player()
#print(a.read_position())

class Field:
    """
    False = empty;
    class_object = saved ship part
    x = crashed part of ship
    o = missed shots"""
    def __init__(self):
        self.__ships = [[False] * 10 for i in range(10)]
        self.add_ship()

    def has_ships(self):
        for y_coord in self.__ships:
            for x_coord in y_coord:
                if x_coord not in (False, "x", "o"):
                    return True
        return False

    def shoot_at(self, tuple_):
        if self.__ships[tuple_[0]][tuple_[1]] == "x" or self.__ships[tuple_[0]][tuple_[1]] == "o":
            return None
        elif self.__ships[tuple_[0]][tuple_[1]]:
            self.__ships[tuple_[0]][tuple_[1]] = "x"
            self.__ships[tuple_[0]][tuple_[1]].shoot_at(tuple_)
            return True
        else:
            self.__ships[tuple_[0]][tuple_[1]] = "o"
            return False

    def field_with_ships(self):
        str_ship = ""
        for y_coord in self.__ships:
            for x_coord in y_coord:
                if x_coord == "x" or x_coord == "o":
                    str_ship += x_coord
                elif x_coord:
                    str_ship += "*"
                else:
                    str_ship += " "
            str_ship += "\n"
        return str_ship[:-2]

    def field_without_ships(self):
        str_ship = ""
        for y_coord in self.__ships:
            for x_coord in y_coord:
                if x_coord == "x" or x_coord == "o":
                    str_ship += x_coord
                else:
                    str_ship += " "
            str_ship += "\n"
        return str_ship[:-2]

    def add_ship(self):
        import random
        for ships in range(4):
            for ship in range(ships + 1):
                while True:
                    checker = False
                    horizontal = random.choice((True, False))
                    if horizontal:
                        bow = (random.randrange(0, 7 + ships), random.randrange(0, 10))
                        for width in range(-1, 5 - ships):
                            if not (0 <= bow[0] + width <= 9): continue
                            for height in range(-1, 2):
                                if not (0 <= bow[1] + height <= 9): continue
                                if self.__ships[bow[0] + width][bow[1] + height]:
                                    checker = True
                                    break
                            if checker:
                                break
                    else:
                        bow = (random.randrange(0, 10), random.randrange(0, 7 + ships))
                        for height in range(-1, 5 - ships):
                            if not (0 <= bow[1] + height <= 9): continue
                            for width in range(-1, 2):
                                if not (0 <= bow[0] + width <= 9): continue
                                if self.__ships[bow[0] + width][bow[1] + height]:
                                    checker = True
                                    break
                            if checker:
                                break
                    if not checker:
                        break
                new_ship = Ship(length=(1, 4 - ships), horizontal=horizontal, bow=bow)
                for coord in new_ship.generate_parts():
                    self.__ships[coord[0]][coord[1]] = new_ship


class Ship:
    def __init__(self, length=(0, 0), bow=(0, 0), horizontal=True):
        self.bow = bow
        self.horizontal = horizontal
        self.__length = length
        self.__hit = [False] * length[1]

    def shoot_at(self, tuple_):
        if self.horizontal:
            self.__hit[tuple_[0] - self.bow[0]] = True
        else:
            self.__hit[tuple_[1] - self.bow[1]] = True

    def generate_parts(self):
        parts = set()
        if self.horizontal:
            for coord in range(self.bow[0], self.bow[0] + self.__length[1]):
                parts.add((coord, self.bow[1]))
        else:
            for coord in range(self.bow[1], self.bow[1] + self.__length[1]):
                parts.add((self.bow[0], coord))
        return parts
a = Game()
a.play_game()
