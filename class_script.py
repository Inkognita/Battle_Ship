class Game:
    def __init__(self):
        self.__fields = list()
        self.__players = list()
        self.__curent_player = 0

    @staticmethod
    def custom_print(fields, texts):
        str_res = ""
        for sent in texts:
            str_res += sent.center(22) + 5 * " "
        str_res += "\n" + "   A|B|C|D|E|F|G|H|I|J|     " * len(texts) + "\n"
        for y_coord in range(10):
            str_res += str(y_coord + 1).center(2) + "|"
            for x_coord in range(10):
                str_res += fields[0][10 * y_coord + x_coord] + "|"
            str_res += "     "
            #str_res += "\n"
            if len(fields) != 1:
                str_res += str(y_coord + 1).center(2) + "|"
                for x_coord in range(10):
                    str_res += fields[1][10 * y_coord + x_coord] + "|"
            str_res += "\n"
        return str_res

    def play_game(self):
        input("Please press enter to start...")
        for i in range(2):
            self.add_player()
            input("Press enter to see your field...")
            #print(self.field_with_ships(self.__curent_player))
            print(self.custom_print([self.field_with_ships(self.__curent_player)], ["Your Field"]))
            input("Press enter")
            print(10 * "\n")
            self.__curent_player += 1
        while True:
            for i, k in ((1, 2), (2, 1)):
                result_shot = (True, 0)
                while result_shot[0] == True:
                    print("Player {0} is playing".format(self.__players[i - 1]._Player__name))
                    input("Press enter to see ...")
                    print(self.custom_print([self.field_without_ships(k - 1), self.field_with_ships(i - 1)],
                                            ["Enemy's field", "Your Field=)"]))
                    #print("Enemy's field\n{0}".format(self.field_without_ships(k - 1)))
                    #print("Your field\n{0}".format(self.field_with_ships(i - 1)))
                    result_shot = self.shoot_at(k - 1, self.__players[0].read_position())
                    while result_shot[0] == None:
                        print("You were shooting this field, try again")
                        print("Enemy's field\n{0}".format(self.field_without_ships(k - 1)))
                        result_shot = self.shoot_at(k - 1, self.__players[0].read_position())
                    if result_shot[0] == True:
                        if result_shot[1] == 1:
                            if self.__fields[k-1].has_ships():
                                print("You crashed it=)")
                            else:
                                return "Player {0} Won".format(self.__players[i - 1]._Player__name)
                        else:
                            print("You damaged it...")
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
        input_ = input("Type coordinate of type C1: ").strip()
        while True:
            try:
                x, y = input_[0], int(input_[1:])
                break
            except:
                input_ = input("Type C1 or B2 or A1: ").strip()
        return y - 1, ord(x.upper()) - 65

class Field:
    def __init__(self):
        self.__ships = [[False] * 10 for i in range(10)]
        #self.__ships = [[" "] * 10 for i in range(10)]
        self.add_ship()

    def has_ships(self):
        for y_coord in range(10):
            for x_coord in range(10):
                if type(self.__ships[y_coord][x_coord]) == Ship:
                    if not self.__ships[y_coord][x_coord].is_damaged((y_coord, x_coord)):
                        return True
        return False

    def shoot_at(self, tuple_):
        if not self.__ships[tuple_[0]][tuple_[1]]:
            self.__ships[tuple_[0]][tuple_[1]] = "o"
            return False, 0
        elif self.__ships[tuple_[0]][tuple_[1]] == "o":
            return None, 0
        elif type(self.__ships[tuple_[0]][tuple_[1]]) == Ship:
            if self.__ships[tuple_[0]][tuple_[1]].is_damaged(tuple_):
                return None, 0
            else:
                if self.__ships[tuple_[0]][tuple_[1]].shoot_at(tuple_):
                    return True, 1
                else:
                    return True, 0

    def field_with_ships(self):
        str_ship = ""
        for y_coord in range(10):
            for x_coord in range(10):
                if self.__ships[y_coord][x_coord] == "o":
                    str_ship += "o"
                elif type(self.__ships[y_coord][x_coord]) == Ship:
                    if self.__ships[y_coord][x_coord].is_damaged((y_coord, x_coord)):
                        str_ship += "x"
                    else:
                        str_ship += "*"
                else:
                    str_ship += " "
            #str_ship += "\n"
        return str_ship

    def field_without_ships(self):
        str_ship = ""
        for y_coord in range(10):
            for x_coord in range(10):
                if self.__ships[y_coord][x_coord] == "o":
                    str_ship += "o"
                elif type(self.__ships[y_coord][x_coord]) == Ship:
                    if self.__ships[y_coord][x_coord].is_damaged((y_coord, x_coord)):
                        str_ship += "x"
                    else:
                        str_ship += " "
                else:
                    str_ship += " "
            #str_ship += "\n"
        return str_ship

    def add_ship(self):
        import random
        for ship_size in range(4):
            for do_iter in range(ship_size + 1):
                while True:
                    checker = False
                    horizontal = random.choice((True, False))
                    if horizontal:
                        bow = (random.randrange(0, 10), random.randrange(0, 7 + ship_size))
                        for width in range(-1, 5 - ship_size):
                            if not (0 <= bow[1] + width <= 9): continue
                            for height in range(-1, 2):
                                if not (0 <= bow[0] + height <= 9): continue
                                if self.__ships[bow[0] + height][bow[1] + width]:
                                    checker = True
                                    break
                            if checker:
                                break
                    else:
                        bow = (random.randrange(0, 7 + ship_size), random.randrange(0, 10))
                        for height in range(-1, 5 - ship_size):
                            if not (0 <= bow[0] + height <= 9): continue
                            for width in range(-1, 2):
                                if not (0 <= bow[1] + width <= 9): continue
                                if self.__ships[bow[0] + height][bow[1] + width]:
                                    checker = True
                                    break
                            if checker:
                                break
                    if not checker:
                        break
                new_ship = Ship(length=(1, 4 - ship_size), horizontal=horizontal, bow=bow)
                if horizontal:
                    for width in range(4 - ship_size):
                        self.__ships[bow[0]][bow[1] + width] = new_ship
                        #self.__ships[bow[0]][bow[1] + width] = "*"
                else:
                    for height in range(4 - ship_size):
                        #self.__ships[bow[0] + height][bow[1]] = "*"
                        self.__ships[bow[0] + height][bow[1]] = new_ship

#a = Field()
class Ship:
    def __init__(self, length=(0, 0), bow=(0, 0), horizontal=True):
        self.bow = bow
        self.horizontal = horizontal
        self.__length = length
        self.__hit = [False] * length[1]

    def shoot_at(self, tuple_):
        indicator = tuple_[1] - self.bow[1] if self.horizontal else tuple_[0] - self.bow[0]
        self.__hit[indicator] = True
        if self.__hit == self.__length[1] * [True]:
            return True
        else:
            return False

    def is_damaged(self, tuple_):
        indicator = tuple_[1] - self.bow[1] if self.horizontal else tuple_[0] - self.bow[0]
        if self.__hit[indicator]:
            return True
        else:
            return False
a = Game()
a.play_game()