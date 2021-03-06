'''Classes for Mario'''
import os
import signal

from alarmexception import AlarmException
from getch import _getChUnix as getChar
from globals import NUM_STONE_ROWS


class Mario():
    '''Class For Mario'''

    def __init__(self):
        self._str = []
        self.pos = []
        self.direction = ""
        self._str.append(['*'])
        self._str.append(['|'])
        self.direction = "right"
        self.pos.append(NUM_STONE_ROWS[0] - 2)
        self.legs_pos = NUM_STONE_ROWS[0] - 1
        self.pos.append(5)

    def move_left(
            self,
            base_level_prev,
            base_level,
            canvas,
            begin,
            board,
            enemy_list,
            boss,
            score):
        '''Make Mario to the left'''
        os.system("tput reset")
        if base_level_prev >= base_level:
            begin[0] -= 1
            canvas[base_level + self.pos[0]][begin[0] + self.pos[1] + 1] = ' '
            canvas[base_level + self.pos[0] +
                   1][begin[0] + self.pos[1] + 1] = ' '
            self.direction = "left"
        for enemy in enemy_list:
            enemy.oscillate()
            enemy.draw(canvas)
        self.checks(canvas=canvas, boss=boss, begin=begin, score=score)
        board.draw(begin)

    def move_right(
            self,
            base_level_next,
            base_level,
            canvas,
            begin,
            board,
            enemy_list,
            boss,
            score):
        '''Make mario move to the right'''
        os.system("tput reset")
        if base_level_next >= base_level:
            begin[0] += 1
            canvas[base_level + self.pos[0]
                  ][begin[0] + self.pos[1] - 1] = ' '
            canvas[base_level + self.pos[0] +
                   1][begin[0] + self.pos[1] - 1] = ' '
            self.direction = "right"
        boss.oscillate()
        for enemy in enemy_list:
            enemy.oscillate()
            enemy.draw(canvas)
        boss.draw(canvas)
        board.draw(begin)

    def draw(self, canvas, begin, base_level):
        '''Draw Mario on the canvas'''
        for i in range(len(self._str)):
            for j in range(len(self._str[i])):
                canvas[base_level + self.pos[0] + i][begin[0] +
                                                     self.pos[1] + j] = self._str[i][j]

    def jump_right(self, canvas, begin, base_level, enemy_list, coin_list, score, boss, board, use):
        '''Make mario jump to the right'''
        os.system("aplay ./jump.wav &")
        for i in range(5 - base_level):
            i += 1
            i -= 1
            os.system("tput reset")
            begin[0] += 1
            self.pos[0] -= 1
            canvas[base_level + self.pos[0] +
                   1][begin[0] + self.pos[1] - 1] = ' '
            canvas[base_level + self.pos[0] +
                   2][begin[0] + self.pos[1] - 1] = ' '
            canvas[base_level + self.pos[0]
                  ][begin[0] + self.pos[1]] = "*"
            canvas[base_level + self.pos[0] +
                   1][begin[0] + self.pos[1]] = "|"
            for enemy in enemy_list:
                enemy.oscillate()
                enemy.draw(canvas)
            for coi in coin_list:
                if coi.check(mario=self, begin=begin):
                    coin_list.remove(coi)
                    score[0] += 1
            self.checks(
                canvas=canvas,
                boss=boss,
                begin=begin,
                score=score)
            board.draw(begin)
            char = use()
        for i in range(5 - base_level):
            os.system("tput reset")
            begin[0] += 1
            self.pos[0] += 1
            canvas[base_level + self.pos[0] -
                   1][begin[0] + self.pos[1] - 1] = ' '
            canvas[base_level + self.pos[0]
                  ][begin[0] + self.pos[1] - 1] = ' '
            canvas[base_level + self.pos[0]
                  ][begin[0] + self.pos[1]] = "*"
            canvas[base_level + self.pos[0] +
                   1][begin[0] + self.pos[1]] = "|"
            for enemy in enemy_list:
                if self.legs_pos == enemy.pos_y and self.pos[1] + \
                        begin[0] == enemy.pos_x:
                    enemy_list.remove(enemy)
                    score[0] += 10
                else:
                    enemy.draw(canvas)
                    enemy.oscillate()
            for coi in coin_list:
                if coi.check(mario=self, begin=begin):
                    coin_list.remove(coi)
                    score[0] += 1
            self.checks(
                canvas=canvas,
                boss=boss,
                begin=begin,
                score=score)
            board.draw(begin)
            char = use()

    def jump_left(self, canvas, begin, base_level, enemy_list, coin_list, score, boss, board, user_input):
        '''Make mario jump to the left'''
        os.system("aplay ./jump.wav &")
        for i in range(5 - base_level):
            os.system("tput reset")
            begin[0] -= 1
            self.pos[0] -= 1
            canvas[base_level + self.pos[0] + 1][base_level +
                                                 begin[0] + self.pos[1] + 1] = ' '
            canvas[base_level + self.pos[0] +
                   2][begin[0] + self.pos[1] + 1] = ' '
            canvas[base_level + self.pos[0]
                  ][begin[0] + self.pos[1]] = "*"
            canvas[base_level + self.pos[0] +
                   1][begin[0] + self.pos[1]] = "|"
            for enemy in enemy_list:
                if self.legs_pos == enemy.pos_y and self.pos[1] + \
                        begin[0] == enemy.pos_x:
                    enemy_list.remove(enemy)
                    score[0] += 10
                else:
                    enemy.draw(canvas)
                    enemy.oscillate()
            for coi in coin_list:
                if coi.check(mario=self, begin=begin):
                    coin_list.remove(coi)
                    score[0] += 1
            self.checks(
                canvas=canvas,
                boss=boss,
                begin=begin,
                score=score)
            board.draw(begin)
            char = user_input()

        for i in range(5 - base_level):
            os.system("tput reset")
            begin[0] -= 1
            self.pos[0] += 1
            canvas[base_level + self.pos[0] -
                   1][begin[0] + self.pos[1] + 1] = ' '
            canvas[base_level + self.pos[0]
                  ][begin[0] + self.pos[1] + 1] = ' '
            canvas[base_level + self.pos[0]
                  ][begin[0] + self.pos[1]] = "*"
            canvas[base_level + self.pos[0] +
                   1][begin[0] + self.pos[1]] = "|"
            for enemy in enemy_list:
                if self.legs_pos == enemy.pos_y and self.pos[1] + \
                        begin[0] == enemy.pos_x:
                    enemy_list.remove(enemy)
                    score[0] += 10
                else:
                    enemy.draw(canvas)
                    enemy.oscillate()
            for coi in coin_list:
                if coi.check(mario=self, begin=begin):
                    coin_list.remove(coi)
                    score[0] += 1
            self.checks(
                canvas=canvas,
                boss=boss,
                begin=begin,
                score=score)
            board.draw(begin)
            char = user_input()

    def checks(self, canvas, boss, begin, score):
        '''Check Mario and Boss interaction'''
        boss.check(mario=self, begin=begin, score=score)
        boss.oscillate()
        boss.draw(canvas)

    def move_mario(self, args):
        '''Move Mario'''
        board = args["board"]
        canvas = args["canvas"]
        begin = args["begin"]
        enemy_list = args["enemy_list"]
        score = args["score"]
        base_level = args["base_level"]
        base_level_next = args["base_level_next"]
        base_level_prev = args["base_level_prev"]
        boss = args["boss"]
        coin_list = args["coin_list"]

        def alarmhandler(signum, frame):
            ''' input method '''
            raise AlarmException

        def user_input(timeout=0.1):
            ''' input method '''
            signal.signal(signal.SIGALRM, alarmhandler)
            signal.setitimer(signal.ITIMER_REAL, timeout)
            try:
                text = getChar()()
                signal.alarm(0)
                return text
            except AlarmException:
                pass
            signal.signal(signal.SIGALRM, signal.SIG_IGN)
            return ''

        char = user_input()

        if char == 'q':
            os.system("fuser -k -TERM ./theme.wav")
            quit()

        if char == 'd':
            self.move_right(base_level_next, base_level, canvas,
                            begin, board, enemy_list, boss, score)

        if char == 'a':
            self.move_left(
                base_level_prev,
                base_level,
                canvas,
                begin,
                board,
                enemy_list,
                boss,
                score)

        if char == 'w':
            if self.direction == "right":
                self.jump_right(canvas, begin, base_level, enemy_list,
                                coin_list, score, boss, board, user_input)

            if self.direction == "left":
                self.jump_left(canvas, begin, base_level, enemy_list,
                               coin_list, score, boss, board, user_input)
