import sys
import random
from hmac_sha256 import HMAC
from table_generator import TableGenerator
from winner import Winner

class Game:
    def __init__(self, moves):
        self.moves = moves
        self.pc_move = random.choice(moves)
        self.hmac = HMAC(self.pc_move)

    def print_menu(self):
        print()
        print(f'HMAC: {self.hmac.hexdigest}')
        print('Available moves:')
        for i, move in enumerate(self.moves):
            print(f'{i+1} - {move}')
        print('0 - exit')
        print('? - help')

    def get_user_move(self):
        return input('Enter your move: ')

    def run(self):
        while True:
            self.print_menu()
            user_move_sym = self.get_user_move()
            self.user_move = self.process_user_move(user_move_sym)
            if self.user_move: break

        winner = Winner().calculate_winner(self.pc_move, self.user_move, self.moves)
        self.announce_winner(winner)

        
    def process_user_move(self, user_move_sym):
        if user_move_sym == '0':
            exit()
        
        if user_move_sym == '?':
            TableGenerator(self.moves).print_table()
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
    