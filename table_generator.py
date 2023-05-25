from prettytable import PrettyTable
from winner import Winner

class TableGenerator:
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