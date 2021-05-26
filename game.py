import pygame
import sys
import random
from board import Board
from ai import DebugAI, AI

pygame.init()
pygame.display.set_caption('Palich Szymon XO')
pygame.display.set_icon(pygame.image.load("assets/icon.png"))


class Game:
    DEFAULT_AI = "AI"
    PLAYER_FIRST = True
    BREAK = 500
    BREAK_MIN = 250
    WHITE_COLOR = 255, 255, 255
    BOTTOM_PANEL = pygame.image.load("assets/bottom_panel.png")
    BTN_RESTART = pygame.image.load("assets/btn_restart.png")
    BTN_RESTART_RECT = pygame.Rect(100, 600, 280, 60)
    BTN_QUIT = pygame.image.load("assets/btn_quit.png")
    BTN_QUIT_RECT = pygame.Rect(100, 680, 280, 60)
    BOARD_IMAGE = pygame.image.load("assets/board.png")
    BLANK = pygame.image.load("assets/blank.png")
    KOLKO = pygame.image.load("assets/kolko.png")
    KOLKO_HIGHLIGHT = pygame.image.load("assets/kolko_highlight.png")
    KRZYZYK = pygame.image.load("assets/krzyzyk.png")
    KRZYZYK_HIGHLIGHT = pygame.image.load("assets/krzyzyk_highlight.png")
    W_TOKU = pygame.image.load("assets/w_toku.png")
    REMIS = pygame.image.load("assets/remis.png")
    PRZEGRANA = pygame.image.load("assets/przegrana.png")
    WYGRANA = pygame.image.load("assets/wygrana.png")

    RECTS = [[(0, 0), (164, 0), (328, 0)],
             [(0, 164), (164, 164), (328, 164)],
             [(0, 328), (164, 328), (328, 328)]]

    def __init__(self):
        self.turn = 1
        if self.DEFAULT_AI == "DebugAI":
            self.ai = DebugAI()
        else:
            self.ai = AI()
        self.board = Board()
        self.curr_choice = None
        self.game_width, self.game_height = 480, 768
        self.board_width, self.board_height = 480, 480
        self.bottom_width, self.bottom_height = 480, 288
        self.screen = pygame.display.set_mode((self.game_width, self.game_height))
        if random.randint(0, 1):
            self.PLAYER_FIRST = True
        else:
            self.PLAYER_FIRST = False
        self.start()
        self.mainloop()

    def draw(self):
        board_x = 0
        for x in self.board.board:
            board_y = 0
            for y in x:
                if y == "x":
                    self.screen.blit(self.KRZYZYK, (self.RECTS[board_x][board_y][0], self.RECTS[board_x][board_y][1]))
                elif y == "o":
                    self.screen.blit(self.KOLKO, (self.RECTS[board_x][board_y][0], self.RECTS[board_x][board_y][1]))
                board_y += 1
            board_x += 1
        pygame.display.flip()

    def highlight(self, pos, player):
        to_blit = None
        if player == "x":
            to_blit = self.KRZYZYK_HIGHLIGHT
        elif player == "o":
            to_blit = self.KOLKO_HIGHLIGHT
        self.screen.blit(to_blit, (self.RECTS[pos[0]][pos[1]][0], self.RECTS[pos[0]][pos[1]][1]))
        pygame.display.flip()

    def highlight_stop(self, pos, player):
        to_blit = None
        if player == "x":
            to_blit = self.KRZYZYK
        elif player == "o":
            to_blit = self.KOLKO
        self.screen.blit(to_blit, (self.RECTS[pos[0]][pos[1]][0], self.RECTS[pos[0]][pos[1]][1]))
        pygame.display.flip()

    def clear_elm(self, pos):
        self.screen.blit(self.BLANK, (self.RECTS[pos[0]][pos[1]][0], self.RECTS[pos[0]][pos[1]][1]))
        self.board.board[pos[0]][pos[1]] = "0"
        pygame.display.flip()

    def clear(self):
        self.screen.blit(self.BOARD_IMAGE, (0, 0))
        self.screen.blit(self.W_TOKU, (100, 520))
        pygame.display.flip()

    def get_position(self, pos):
        board_x = 0
        for x in self.RECTS:
            board_y = 0
            for y in x:
                if pygame.Rect(y[0], y[1], 152, 152).collidepoint(pos):
                    new_pos = (board_x, board_y)
                    return new_pos
                board_y += 1
            board_x += 1

    def make_move(self, pos, player):
        if player == "x":
            self.board.make_move(player, (pos[0], pos[1]))
        elif player == "o":
            self.board.make_move(player, (pos[0], pos[1]))
        self.draw()

    def show_status(self, status):
        if status == "x":
            self.screen.blit(self.WYGRANA, (100, 520))
        elif status == "o":
            self.screen.blit(self.PRZEGRANA, (100, 520))
        else:
            self.screen.blit(self.REMIS, (100, 520))
        pygame.display.flip()

    def start(self):
        self.screen.fill(self.WHITE_COLOR)
        self.screen.blit(self.BOARD_IMAGE, (0, 0))
        self.screen.blit(self.BOTTOM_PANEL, (0, 480))
        self.screen.blit(self.W_TOKU, (100, 520))
        self.screen.blit(self.BTN_RESTART, (100, 600))
        self.screen.blit(self.BTN_QUIT, (100, 680))
        if not self.PLAYER_FIRST:
            cords = self.ai.next_turn(self.board, None)
            if cords is not None:
                pygame.time.wait(self.BREAK_MIN)
                self.make_move(cords, "o")
        pygame.display.flip()

    def restart(self):
        if random.randint(0, 1):
            self.PLAYER_FIRST = True
        else:
            self.PLAYER_FIRST = False
        self.turn = 1
        if self.DEFAULT_AI == "DebugAI":
            self.ai = DebugAI()
        else:
            self.ai = AI()
        self.board = Board()
        self.curr_choice = None
        self.clear()
        if not self.PLAYER_FIRST:
            cords = self.ai.next_turn(self.board, None)
            if cords is not None:
                pygame.time.wait(self.BREAK_MIN)
                self.make_move(cords, "o")

    def mainloop(self):
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    pos = self.get_position(mouse_pos)
                    if self.BTN_RESTART_RECT.collidepoint(mouse_pos):
                        self.restart()
                    elif self.BTN_QUIT_RECT.collidepoint(mouse_pos):
                        sys.exit()
                    elif pos is not None and self.turn == 3 and not self.PLAYER_FIRST:
                        if self.board.check_if_move_is_possible(pos):  # ruchy
                            self.make_move(pos, "x")
                            prev_cords, cords = self.ai.next_turn(self.board, pos)
                            self.board.clear(prev_cords)
                            if cords is not None:
                                self.highlight(prev_cords, "o")
                                pygame.time.wait(self.BREAK)
                                self.clear_elm(prev_cords)
                                self.make_move(cords, "o")
                                self.highlight(cords, "o")
                                pygame.time.wait(self.BREAK)
                                self.highlight_stop(cords, "o")
                                self.turn += 1
                    elif self.curr_choice is not None and pos is not None and \
                            self.board.check_if_last_move_is_possible(self.curr_choice, pos):  # ruchy
                        self.clear_elm(self.curr_choice)
                        self.curr_choice = None
                        self.make_move(pos, "x")
                        if self.PLAYER_FIRST:
                            prev_cords, cords = self.ai.next_turn(self.board, pos)
                            if cords is not None:
                                self.highlight(prev_cords, "o")
                                pygame.time.wait(self.BREAK)
                                self.clear_elm(prev_cords)
                                self.make_move(cords, "o")
                                self.highlight(cords, "o")
                                pygame.time.wait(self.BREAK)
                                self.highlight_stop(cords, "o")

                        self.show_status(self.board.check_win())
                        self.turn += 1
                    elif pos is not None and self.turn == 4 and self.curr_choice == pos:
                        self.curr_choice = None
                        self.highlight_stop(pos, "x")
                    elif pos is not None and self.turn == 4 and self.board.check_if_is_player(pos):
                        if self.curr_choice is not None:
                            self.highlight_stop(self.curr_choice, "x")
                        self.curr_choice = pos
                        self.highlight(pos, "x")
                    elif pos is not None and self.turn < 5:
                        if self.turn < 4 and self.board.check_if_move_is_possible(pos):  # ruchy
                            self.make_move(pos, "x")
                            cords = self.ai.next_turn(self.board, pos)
                            if cords is not None:
                                pygame.time.wait(self.BREAK_MIN)
                                self.make_move(cords, "o")
                            self.turn += 1


if __name__ == '__main__':
    Game()
