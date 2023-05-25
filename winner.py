
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