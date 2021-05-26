class Board:
    def __init__(self):
        self.board = [[0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]]

    def check_if_is_player(self, cords):
        if self.board[cords[0]][cords[1]] == "x":
            return True

    def check_if_move_is_possible(self, cords):
        if self.board[cords[0]][cords[1]] == 0 or self.board[cords[0]][cords[1]] == "0":
            return True

    def check_if_last_move_is_possible(self, cords_start, cords_end):
        if (self.board[cords_end[0]][cords_end[1]] == 0 or self.board[cords_end[0]][cords_end[1]] == "0") and \
                (cords_start[0] == cords_end[0] or cords_start[1] == cords_end[1]):
            return True

    def make_move(self, player, cords):
        self.board[cords[0]][cords[1]] = player

    def get_pos(self, cords):
        return self.board[cords[0]][cords[1]]

    def clear(self, cords):
        self.board[cords[0]][cords[1]] = str(0)

    def check_win(self):
        wins = {
            "x": 0,
            "o": 0
        }

        for x in range(3):
            stat = ""
            for y in range(3):
                stat += str(self.board[x][y])
            if stat == "xxx":
                wins["x"] += 1
            elif stat == "ooo":
                wins["o"] += 1

        for x in range(3):
            stat = ""
            for y in range(3):
                stat += str(self.board[y][x])
            if stat == "xxx":
                wins["x"] += 1
            elif stat == "ooo":
                wins["o"] += 1

        stat = ""
        for x in range(3):
            for y in range(3):
                if x == y:
                    stat += str(self.board[y][x])
        if stat == "xxx":
            wins["x"] += 1
        elif stat == "ooo":
            wins["o"] += 1

        stat = ""
        n = 2
        for x in range(3):
            for y in range(3):
                if y == n:
                    stat += str(self.board[y][x])
                    n -= 1
        if stat == "xxx":
            wins["x"] += 1
        elif stat == "ooo":
            wins["o"] += 1

        if wins["x"] == wins["o"] == 1:
            return "rm"
        elif wins["x"] == 1:
            return "x"
        elif wins["o"] == 1:
            return "o"
        else:
            return "rm"
