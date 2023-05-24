import sys
import random
import hashlib
import hmac
import secrets
from prettytable import PrettyTable

class HMAC:
    def __init__(self, message):
        self.secret_key = secrets.token_hex(32).upper()
        self.message = message
        self.hexdigest = self.get_hmac(self.secret_key, message).upper()
    
    def get_hmac(self, secret_key, message):
        secret_key = secret_key.encode()
        message = message.encode()
        return hmac.new(secret_key, message, hashlib.sha256).hexdigest()


class Winner():
    def calculate_winner(self, pc_move, user_move, moves):
        if pc_move == user_move: return

        pc_move_index = moves.index(pc_move)
        user_move_index = moves.index(user_move)
        half = len(moves) // 2
        end_index = user_move_index+1 + half

        if pc_move in moves[user_move_index+1 : end_index]:
            return pc_move

        if end_index > len(moves):
            end_index = end_index - len(moves)

            if pc_move in moves[user_move_index+1 : ] or \
            pc_move in moves[ : end_index]:
                return pc_move

        return user_move


class Game:
    def __init__(self, moves):
        self.moves = moves
        self.pc_move = random.choice(moves)
        self.hmac = HMAC(self.pc_move)

    def get_user_move(self):
        print()
        print(f'HMAC: {self.hmac.hexdigest}')
        print('Available moves:')
        for i, move in enumerate(self.moves):
            print(f'{i+1} - {move}')
        print('0 - exit')
        print('? - help')
        return input('Enter your move: ')

    def run(self):
        while True:
            user_move_sym = self.get_user_move()
            self.user_move = self.process_user_move(user_move_sym)
            if self.user_move: break

        winner = Winner().calculate_winner(self.pc_move, self.user_move, self.moves)
        self.announce_winner(winner)

        
    def process_user_move(self, user_move_sym):
        if user_move_sym == '0':
            exit()
        
        if user_move_sym == '?':
            GenerateTable(self.moves).print_table()
            return

        if not user_move_sym.isdigit():
            return

        if int(user_move_sym) > len(self.moves):
            return
        
        user_move = self.moves[int(user_move_sym)-1]
        return user_move

    def announce_winner(self, winner):
        print(f'Your move: {self.user_move}')
        print(f'Computer move: {self.pc_move}')

        if winner == self.user_move:
            print('You win!')
        if winner == self.pc_move:
            print('Computer wins!')
        if not winner:
            print('It`s a draw!')

        print(f'HMAC key: {self.hmac.secret_key}')


class GenerateTable:
    def __init__(self, moves):
        self.moves = moves

    def print_table(self):
        print()
        print('Table describes who wins.')
        table = PrettyTable()
        header = ['', *self.moves]
        table.field_names = header

        for i in self.moves:
            row = [i]
            for x in self.moves:
                winner = Winner().calculate_winner(i, x, self.moves)
                if not winner: 
                    winner = 'draw'
                row.append(winner)
            table.add_row(row)

        print(table)
        
def check_moves(moves):
    if len(moves) < 3:
        print(f'You should pass 3 or more moves. You have passed {len(moves)} moves.')
        return False

    if not len(moves) % 2:
        print(f'You should pass an odd number of moves. You have passed {len(moves)} moves.')
        return False
    
    for move in moves:
        if moves.count(move) > 1:
            print(f'Passed moves should be unique. "{move}" have been passed {moves.count(move)} times')
            return False
    
    return True


if __name__ == '__main__':

    moves = sys.argv[1:]
    if not check_moves(moves): exit()
    
    game = Game(moves)
    game.run()
    