# Copyright 2020 Rodrigo Pietnechuk

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

from collections.abc import MutableSequence
from typing import Any

class Board(MutableSequence):
    """Represents the game board."""
    def __init__(self, rows:int=7, columns:int=7):
        """Class constructor.
        
        Creates a nested list containing {self.columns} empty lists.
        """
        self.rows = rows
        self.columns = columns

        super(Board, self).__init__()
        self._list = list()

        for i in range(columns):
            self._list.append(list())

    def clear_board(self) -> None:
        """Clears the game board to start a new game."""
        return map(lambda col: col.clear(), self._list)

    def insert(self, index:int, element) -> None:
        """Inserts an element in the board."""
        return self._list.insert(index, element)

    def __delitem__(self, index:int) -> None:
        """Deletes an element from the board."""
        del self._list[index]
    
    def __getitem__(self, index:int) -> Any:
        """Gets the value of an element of the board."""
        return self._list.__getitem__(index)

    def __len__(self) -> int:
        """Returns the lenght of the board."""
        return len(self._list)

    def __setitem__(self, index:int, element:Any) -> None:
        """Sets the object element in the board index index."""
        return self._list.__setitem__(index, element)

    def __str__(self) -> str:
        """Returns the board as a string."""
        string = ""
        for i in range(self.rows-1, -1, -1):
            for j in range(self.columns):
                try:
                    string += str(self._list[j][i]) + " "
                except IndexError:
                    string += "- "
            string += "\n"
        return string

class Player:
    """Represents a player of the game."""
    def __init__(self, name:str, symbol:str):
        """Class constructor.

        Creates a player with a name and a symbol, and a default score of 0.
        """
        self.name = name
        self.symbol = symbol
        self.score = 0

class FourInRow(Board):
    """Represents the game itself, consisting of a board and two players."""
    def __init__(self, rows:int=7, columns:int=7):
        self.tie_score = 0

        super().__init__(rows, columns)

        print("Welcome to 4 in a row!\n")
        self.set_players()
        self.play()

    def set_players(self) -> None:
        """Crates two players to play the match."""
        p1 = Player(name=input("Enter the name of the player 1: "), symbol="1")
        p2 = Player(name=input("Enter the name of the player 2: "), symbol="2")
        self.__players = [p1, p2]

    def show_scores(self) -> None:
        """Prints the scores of the match."""
        print("\nScores")
        for player in self.__players:
            print(f"{player.name}: {player.score}")
        print(f"Ties: {self.tie_score}")
    
    def play(self) -> None:
        """Sets a round of the game."""
        self.clear_board()

        while True:
            print(f"\n{self.__players[0].name}'s turn.")
            print(self)

            incorrect_input = True
            col = 0
            while incorrect_input:
                try:
                    col = int(input(f"Select a column number from 1 to {self.columns}: ")) - 1
                    if  not (0 <= col < self.columns) or (len(self._list[col]) == self.rows):
                        raise IndexError
                    self._list[col].append(self.__players[0].symbol)
                except ValueError:
                    print("You have to enter a valid column number.")
                except IndexError:
                    print(f"The selected column does not exist or is full. {self.__players[0].name}, please enter other column number:")
                else:
                    incorrect_input = False

            if self.check_for_winner(self.__players[0], col, len(self._list[col])-1):
                return self.declare_winner(self.__players[0])
            
            if self.check_for_tie():
                return self.declare_tie()
            
            self.__players.reverse()

    def check_for_winner(self, player:Player, column:int, row:int) -> bool:
        """Retuns True if the current player has met victory conditions.
        
        The method searchs for four consecutive symbols of the same type
        in all four directions possible.
        """
        check_for = [player.symbol for i in range(4)]
        
        # vertical check
        vert = self._list[column]
        
        # horizontal check
        hor = []
        for i in range(self.columns):
            try:
                hor.append(self._list[i][row])
            except IndexError:
                hor.append("ph") # placeholder

        # main diagonal check
        # upwards
        diag1 = [self._list[column][row]]
        i, j = column + 1, row + 1
        while (i < self.columns) and (j < self.columns):
            try:
                diag1.append(self._list[i][j])
            except IndexError:
                break
            else:
                i += 1
                j += 1
        # downwards
        i, j = column - 1, row - 1
        while (i >= 0) and (j >= 0):
            try:
                diag1.insert(0, self._list[i][j])
            except IndexError:
                break
            else:
                i -= 1
                j -= 1

        # secondary diagonal check
        # upwards
        diag2 = [self._list[column][row]]
        i, j = column - 1, row + 1
        while (i >= 0) and (j < self.columns):
            try:
                diag2.append(self._list[i][j])
            except IndexError:
                break
            else:
                i -= 1
                j += 1
        # downwards
        i, j = column + 1, row - 1
        while (i < self.columns) and (j >= 0):
            try:
                diag2.insert(0, self._list[i][j])
            except IndexError:
                break
            else:
                i += 1
                j -= 1  

        for direction in [vert, hor, diag1, diag2]:
            if self.are_4_in_a_row(direction, check_for):
                return True
        return False

    def are_4_in_a_row(self, search_in:list, search_for:list) -> bool:
        """Returns True if there are four symbols of the same player in the given direction."""
        for i in range(len(search_in)):
            try:
                if search_in[i:i+4] == search_for:
                    return True
            except IndexError:
                return False
        return False
    
    def check_for_tie(self) -> bool:
        """Returns true if the board is full.
        
        Meant to be executed after self.check_for_winner returns False.
        It makes the tie score in the scoreboard to be rised by 1.
        """
        for column in self._list:
            if len(column) != self.rows:
                return False
        return True

    def declare_winner(self, winner:Player) -> None:
        """Prints a message showing the winner of the round and add a point to them."""
        print(f"\n{winner.name} won!")
        print(self)
        winner.score += 1
        self.show_scores()
        return self.ask_for_rematch()

    def declare_tie(self) -> None:
        """Prints a message declaring a tie and adds a point to the tie score."""
        print("\nMatch tied.")
        print(self)
        self.tie_score += 1
        self.show_scores()
        return self.ask_for_rematch()

    def ask_for_rematch(self) -> None:
        """Asks the players if they want to play another match.
        
        Entering 'y' will result in calling the method to play another round.
        Entering 'n' will end the program
        """
        rematch = ""
        while rematch != "y" and rematch != "n":
            rematch = input("\nPlay again (y/n): ").lower()
        if rematch == "y":
            return self.play()

if __name__ == "__main__":
    FourInRow()