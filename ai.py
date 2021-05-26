import random

_0, _1, _2 = (0, 0), (0, 1), (0, 2)
_3, _4, _5 = (1, 0), (1, 1), (1, 2)
_6, _7, _8 = (2, 0), (2, 1), (2, 2)


class DebugAI:
    def __init__(self):
        self.turn = 1
        self.board = None
        self.enemy_move = None
        self.positions = []

    def next_turn(self, board, enemy_move):
        self.board = board
        self.enemy_move = enemy_move
        if self.turn <= 3:
            return self.turn_default()
        elif self.turn == 4:
            return self.last_turn()
        else:
            return

    def turn_default(self):
        cord_x, cord_y = random.randint(0, 2), random.randint(0, 2)
        while self.board.check_if_move_is_possible((cord_x, cord_y)) is not True:
            cord_x, cord_y = random.randint(0, 2), random.randint(0, 2)
        self.turn += 1
        cords = (cord_x, cord_y)
        self.positions.append(list(cords))
        return cords

    def last_turn(self):
        pick = random.randint(0, 2)
        cord_x, cord_y = random.randint(0, 2), random.randint(0, 2)
        while self.board.check_if_last_move_is_possible(self.positions[pick], (cord_x, cord_y)) is not True:
            pick = random.randint(0, 2)
            cord_x, cord_y = random.randint(0, 2), random.randint(0, 2)
        self.turn += 1
        cords = (cord_x, cord_y)
        return self.positions[pick], cords


class AI:
    def __init__(self):
        self.turn = 1
        self.board = None
        self.enemy_move = None
        self.last_move = None
        self.positions = []

    def next_turn(self, board, enemy_move):
        self.board = board
        self.enemy_move = enemy_move
        if self.turn == 1:
            return self.first_turn_choice()
        elif self.turn == 2:
            return self.second_turn_choice()
        elif self.turn == 3:
            return self.third_turn_choice()
        else:
            return self.last_turn()

    def random_move(self, *args):
        if not args:
            args = [_1, _2, _3, _4, _5, _6, _7, _8]

        return args[random.randint(0, len(args) - 1)]

    def get_not_used(self, *args):
        if not args:
            args = [_1, _2, _3, _4, _5, _6, _7, _8]
        to_return = []
        for x in args:
            if self.board.check_if_move_is_possible(x):
                to_return.append(x)
        return to_return

    def get_neighbors(self, pos, position):
        if position == "col":
            return (pos[0], (pos[1] + 2) % 3), (pos[0], (pos[1] + 1) % 3)
        elif position == "row":
            return ((pos[0] + 2) % 3, pos[1]), ((pos[0] + 1) % 3, pos[1])
        else:
            return (pos[0], (pos[1] + 2) % 3), (pos[0], (pos[1] + 1) % 3), \
                   ((pos[0] + 2) % 3, pos[1]), ((pos[0] + 1) % 3, pos[1])

    def get_possibility(self):
        possibility = ()
        for x in range(3):
            stat = ""
            for y in range(3):
                stat += str(self.board.board[x][y])
                if self.board.board[x][y] == 0:
                    possibility = (x, y)
            if ("oo" in stat or "o0o" in stat) and "x" not in stat:
                return possibility

        for x in range(3):
            stat = ""
            for y in range(3):
                stat += str(self.board.board[y][x])
                if self.board.board[y][x] == 0:
                    possibility = (y, x)
            if ("oo" in stat or "o0o" in stat) and "x" not in stat:
                return possibility

        stat = ""
        for x in range(3):
            for y in range(3):
                if x == y:
                    stat += str(self.board.board[y][x])
                    if self.board.board[x][y] == 0:
                        possibility = (x, y)
        if ("oo" in stat or "o0o" in stat) and "x" not in stat:
            return possibility

        stat = ""
        n = 2
        for x in range(3):
            for y in range(3):
                if y == n:
                    stat += str(self.board.board[y][x])
                    if self.board.board[x][y] == 0:
                        possibility = (x, y)
                    n -= 1
        if ("oo" in stat or "o0o" in stat) and "x" not in stat:
            return possibility

        return False

    def get_possibility_last(self):
        possibility = ()
        for x in range(3):
            stat = ""
            for y in range(3):
                stat += str(self.board.board[x][y])
                if self.board.board[x][y] == 0:
                    possibility = (x, y)
            if ("oo" in stat or "o0o" in stat) and "x" not in stat and possibility != ():
                for z in self.get_neighbors(possibility, "row"):
                    if self.board.board[z[0]][z[1]] == "o":
                        return possibility, z

        for x in range(3):
            stat = ""
            for y in range(3):
                stat += str(self.board.board[y][x])
                if self.board.board[y][x] == 0:
                    possibility = (y, x)
            if ("oo" in stat or "o0o" in stat) and "x" not in stat and possibility != ():
                for z in self.get_neighbors(possibility, "col"):
                    if self.board.board[z[0]][z[1]] == "o":
                        return possibility, z

        stat = ""
        for x in range(3):
            for y in range(3):
                if x == y:
                    stat += str(self.board.board[y][x])
                    if self.board.board[x][y] == 0:
                        possibility = (x, y)
        if ("oo" in stat or "o0o" in stat) and "x" not in stat and possibility != ():
            for z in self.get_neighbors(possibility, "xd"):
                if self.board.board[z[0]][z[1]] == "o":
                    return possibility, z

        stat = ""
        n = 2
        for x in range(3):
            for y in range(3):
                if y == n:
                    stat += str(self.board.board[y][x])
                    if self.board.board[x][y] == 0:
                        possibility = (x, y)
                    n -= 1
        if ("oo" in stat or "o0o" in stat) and "x" not in stat and possibility != ():
            for z in self.get_neighbors(possibility, "xd"):
                if self.board.board[z[0]][z[1]] == "o":
                    return possibility, z

        return False

    def check_if_if_enemy_can_win(self):
        for x in range(3):
            stat = ""
            for y in range(3):
                stat += str(self.board.board[x][y])
                if self.board.board[x][y] == 0:
                    possibility = (x, y)
            if "xx" in stat or "x0x" in stat and "o" not in stat:
                return possibility

        for x in range(3):
            stat = ""
            for y in range(3):
                stat += str(self.board.board[y][x])
                if self.board.board[y][x] == 0:
                    possibility = (y, x)
            if "xx" in stat or "x0x" in stat and "o" not in stat:
                return possibility

        stat = ""
        for x in range(3):
            for y in range(3):
                if x == y:
                    stat += str(self.board.board[x][y])
                    if self.board.board[x][y] == 0:
                        possibility = (x, y)
        if "xx" in stat or "x0x" in stat and "o" not in stat:
            return possibility

        stat = ""
        n = 2
        for x in range(3):
            for y in range(3):
                if y == n:
                    stat += str(self.board.board[x][y])
                    if self.board.board[x][y] == 0:
                        possibility = (x, y)
                    n -= 1
        if "xx" in stat or "x0x" in stat and "o" not in stat:
            return possibility

        return False

    def check_if_if_enemy_can_win_last_turn(self):
        possibility = ()
        for x in range(3):
            stat = ""
            for y in range(3):
                stat += str(self.board.board[x][y])
                if self.board.board[x][y] == 0:
                    possibility = (x, y)
            if ("xx" in stat or "x0x" in stat) and "o" not in stat and "xxx" not in stat:
                for z in self.get_neighbors(possibility, "row"):
                    if self.board.board[z[0]][z[1]] == "x":
                        return possibility

        possibility = ()
        for x in range(3):
            stat = ""
            for y in range(3):
                stat += str(self.board.board[y][x])
                if self.board.board[y][x] == 0:
                    possibility = (y, x)
            if ("xx" in stat or "x0x" in stat) and "o" not in stat and "xxx" not in stat:
                for z in self.get_neighbors(possibility, "col"):
                    if self.board.board[z[0]][z[1]] == "x":
                        return possibility

        possibility = ()
        stat = ""
        for x in range(3):
            for y in range(3):
                if x == y:
                    stat += str(self.board.board[x][y])
                    if self.board.board[x][y] == 0:
                        possibility = (x, y)
        if ("xx" in stat or "x0x" in stat) and "o" not in stat and "xxx" not in stat:
            for z in self.get_neighbors(possibility, "all"):
                if self.board.board[z[0]][z[1]] == "x":
                    return possibility

        possibility = ()
        stat = ""
        n = 2
        for x in range(3):
            for y in range(3):
                if y == n:
                    stat += str(self.board.board[x][y])
                    if self.board.board[x][y] == 0:
                        possibility = (x, y)
                    n -= 1
        if ("xx" in stat or "x0x" in stat) and "o" not in stat and "xxx" not in stat:
            for z in self.get_neighbors(possibility, "all"):
                if self.board.board[z[0]][z[1]] == "x":
                    return possibility

        return False

    def check_if_if_possible_to_win_2nd_turn(self):
        possibilities = []

        for x in range(3):
            possibilities_temp = []
            stat = ""
            for y in range(3):
                stat += str(self.board.board[x][y])
                possibilities_temp.append((x, y))
            if "o" in stat and "x" not in stat:
                possibilities += possibilities_temp

        for x in range(3):
            possibilities_temp = []
            stat = ""
            for y in range(3):
                stat += str(self.board.board[y][x])
                possibilities_temp.append((y, x))
            if "o" in stat and "x" not in stat:
                possibilities += possibilities_temp

        possibilities_temp = []
        stat = ""
        for x in range(3):
            for y in range(3):
                if x == y:
                    stat += str(self.board.board[y][x])
                    possibilities_temp.append((x, y))
        if "o" in stat and "x" not in stat:
            possibilities += possibilities_temp

        possibilities_temp = []
        stat = ""
        n = 2
        for x in range(3):
            for y in range(3):
                if y == n:
                    stat += str(self.board.board[y][x])
                    possibilities_temp.append((x, y))
                    n -= 1
        if "o" in stat and "x" not in stat:
            possibilities += possibilities_temp
        if possibilities:
            return possibilities
        else:
            return False

    def first_turn_choice(self):
        if self.enemy_move == _4:
            self.turn += 1
            next_move = self.random_move(_0, _2, _6, _8)
            self.positions.append(next_move)
            return next_move
        else:
            self.turn += 1
            next_move = _4
            self.positions.append(next_move)
            return next_move

    #   0   |   1   |   2
    # ----------------------
    #   3   |   4   |   5
    # ----------------------
    #   6   |   7   |   8

    def second_turn_choice(self):
        comp_chance = self.check_if_if_possible_to_win_2nd_turn()
        enm_chance = self.check_if_if_enemy_can_win()
        if comp_chance:
            next_move = self.random_move(*self.get_not_used(*comp_chance))
        elif enm_chance:
            next_move = enm_chance
        else:
            next_move = self.random_move(*self.get_not_used())
        if self.board.get_pos(_4) == "x":
            if self.enemy_move == _0 and self.board.get_pos(_8) == 0:
                next_move = _8
            elif self.enemy_move == _8 and self.board.get_pos(_0) == 0:
                next_move = _0
            elif self.enemy_move == _2 and self.board.get_pos(_6) == 0:
                next_move = _6
            elif self.enemy_move == _6 and self.board.get_pos(_2) == 0:
                next_move = _2
            else:
                next_move = self.random_move(*self.get_not_used(_8, _6, _2, _0))

        self.last_move = next_move
        self.turn += 1
        self.positions.append(next_move)
        return next_move

    def third_turn_choice(self):
        comp_chance = self.get_possibility()
        enm_chance = self.check_if_if_enemy_can_win_last_turn()
        if enm_chance:
            next_move = enm_chance
        elif comp_chance and self.get_not_used(*self.get_neighbors(comp_chance, "all")):
            next_move = self.random_move(*self.get_neighbors(comp_chance, "all"))
            while not self.board.check_if_move_is_possible(next_move):
                next_move = self.random_move(*self.get_neighbors(comp_chance, "all"))
        else:
            next_move = self.random_move()
            while not self.board.check_if_move_is_possible(next_move):
                next_move = self.random_move()
        self.last_move = next_move
        self.turn += 1
        self.positions.append(next_move)
        return next_move

    def last_turn(self):
        if self.get_possibility_last():
            temp, typ = self.get_possibility_last()
            return typ, temp
        else:
            pick = random.randint(0, 2)
            cord_x, cord_y = random.randint(0, 2), random.randint(0, 2)
            while self.board.check_if_last_move_is_possible(self.positions[pick], (cord_x, cord_y)) is not True:
                pick = random.randint(0, 2)
                cord_x, cord_y = random.randint(0, 2), random.randint(0, 2)
            return self.positions[pick], (cord_x, cord_y)
