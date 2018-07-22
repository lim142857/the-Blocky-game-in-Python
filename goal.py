"""Assignment 2 - Blocky

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto


=== Module Description ===

This file contains the Goal class hierarchy.
"""

from typing import List, Tuple
from block import Block


class Goal:
    """A player goal in the game of Blocky.

    This is an abstract class. Only child classes should be instantiated.

    === Attributes ===
    colour:
        The target colour for this goal, that is the colour to which
        this goal applies.
    """
    colour: Tuple[int, int, int]

    def __init__(self, target_colour: Tuple[int, int, int]) -> None:
        """Initialize this goal to have the given target colour.
        """
        self.colour = target_colour

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given board.

        The score is always greater than or equal to 0.
        """
        raise NotImplementedError

    def description(self) -> str:
        """Return a description of this goal.
        """
        raise NotImplementedError


class BlobGoal(Goal):
    """A goal to create the largest connected blob of this goal's target
    colour, anywhere within the Block.
    """

    def score(self, board: Block) -> int:
        """Return the current score for the blob goal on the given board.

        The score is always greater than or equal to 0.
        """
        visited = []
        max_size = 0
        flattened = board.flatten()
        for i in range(len(flattened)):
            visited.append([])
            for _ in range(len(flattened)):
                visited[i].append(-1)

        for i in range(len(flattened)):
            for j in range(len(flattened)):
                max_size = max(max_size,
                               self._undiscovered_blob_size((i, j),
                                                            flattened,
                                                            visited))
        return max_size

    def description(self) -> str:
        """Return a description of this goal.
        """
        return ' The player must aim for the largest “blob” of a given ' \
               'colour c. A blob is a group of connected blocks with the ' \
               'same colour. Two blocks are connected if their sides touch; ' \
               'touching corners doesn’t count. The player’s score is the ' \
               'number of unit cells in the largest blob of colour c.'

    def _undiscovered_blob_size(self, pos: Tuple[int, int],
                                board: List[List[Tuple[int, int, int]]],
                                visited: List[List[int]]) -> int:
        """Return the size of the largest connected blob that (a) is of this
        Goal's target colour, (b) includes the cell at <pos>, and (c) involves
        only cells that have never been visited.

        If <pos> is out of bounds for <board>, return 0.

        <board> is the flattened board on which to search for the blob.
        <visited> is a parallel structure that, in each cell, contains:
           -1  if this cell has never been visited
            0  if this cell has been visited and discovered
               not to be of the target colour
            1  if this cell has been visited and discovered
               to be of the target colour

        Update <visited> so that all cells that are visited are marked with
        either 0 or 1.
        """
        if pos[0] < 0 or pos[0] >= len(board) \
           or pos[1] < 0 or pos[1] >= len(board):
            return 0
        elif board[pos[0]][pos[1]] != self.colour:
            visited[pos[0]][pos[1]] = 0
            return 0
        elif visited[pos[0]][pos[1]] == 1:
            return 0
        else:
            size = 0
            neighbours = [(pos[0] - 1, pos[1]), (pos[0] + 1, pos[1]),
                          (pos[0], pos[1] - 1), (pos[0], pos[1] + 1)]
            visited[pos[0]][pos[1]] = 1
            for i in neighbours:
                size += self._undiscovered_blob_size(i, board, visited)
            return size + 1


class PerimeterGoal(Goal):
    """A goal to put the most possible units of the goal's target
        colour on the outer perimeter of the board.
        """

    def score(self, board: Block) -> int:
        """Return the current score for the perimeter goal on the given board.

        The score is always greater than or equal to 0.
        """
        score = 0
        flattened = board.flatten()
        length = len(flattened)
        for unit in flattened[0]:
            if unit == self.colour:
                score += 1
        for unit in flattened[length - 1]:
            if unit == self.colour:
                score += 1
        for unit in range(length):
            if flattened[unit][0] == self.colour:
                score += 1
        for unit in range(length):
            if flattened[unit][length - 1] == self.colour:
                score += 1
        return score

    def description(self) -> str:
        """Return a description of the perimeter goal.
        """
        return 'Put the most possible units of the background colour ' \
               'on the outer perimeter of the board.'


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing',
            'block', 'goal', 'player', 'renderer'
        ],
        'max-attributes': 15
    })
