"""Assignment 2 - Blocky: Sample tests

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto


=== Module Description ===

This file contains some sample tests for Assignment 2.
Please use this as a starting point to check your work and write your own
tests!
"""
from typing import List, Tuple
from renderer import COLOUR_LIST
from block import Block
from goal import PerimeterGoal, BlobGoal
from game import Game


def test_flatten() -> None:
    """Test the flatten method of the Block class.

    - Given a properly constructed block structure, flatten to a 2D array
    - Ensure the size is correct (should be 2^{max_depth} by 2^{max_depth})
    - Ensure the content matches the expected content
    """
    # Hand-construct a Block and its correct flattened form.
    board, flatten_expected = construct_board()

    flatten_actual = board.flatten()

    # It should be the case that width == height (we make square boards only)
    assert len(flatten_actual) == len(flatten_actual[0]),\
        'Flattened board should be square.'

    assert len(flatten_actual) == 2**board.max_depth,\
        'Flattened board size should have sides of 2^max_depth.'

    assert flatten_actual == flatten_expected,\
        'Result of flatten is incorrect.'


def test_rectangles_to_draw() -> None:
    """Test the rectangles_to_draw method of the Block class.
    """
    block = Block(0, children=[
        Block(1, children=[
            Block(2, COLOUR_LIST[2]),
            Block(2, COLOUR_LIST[1]),
            Block(2, COLOUR_LIST[2]),
            Block(2, COLOUR_LIST[0])
        ]),
        Block(1, children=[
            Block(2, COLOUR_LIST[0]),
            Block(2, COLOUR_LIST[1]),
            Block(2, COLOUR_LIST[1]),
            Block(2, COLOUR_LIST[2])
        ]),
        Block(1, children=[
            Block(2, COLOUR_LIST[2]),
            Block(2, COLOUR_LIST[1]),
            Block(2, COLOUR_LIST[1]),
            Block(2, COLOUR_LIST[0])
        ]),
        Block(1, children=[
            Block(2, COLOUR_LIST[0]),
            Block(2, COLOUR_LIST[2]),
            Block(2, COLOUR_LIST[1]),
            Block(2, COLOUR_LIST[2])
        ])
    ])
    block.update_block_locations((0, 0), 64)
    expected_rectangles = {
        ((138, 151, 71), (48, 0), (16, 16), 0),
        ((0, 0, 0), (48, 0), (16, 16), 3),
        ((199, 44, 58), (32, 0), (16, 16), 0),
        ((0, 0, 0), (32, 0), (16, 16), 3),
        ((138, 151, 71), (32, 16), (16, 16), 0),
        ((0, 0, 0), (32, 16), (16, 16), 3),
        ((1, 128, 181), (48, 16), (16, 16), 0),
        ((0, 0, 0), (48, 16), (16, 16), 3),
        ((1, 128, 181), (16, 0), (16, 16), 0),
        ((0, 0, 0), (16, 0), (16, 16), 3),
        ((199, 44, 58), (0, 0), (16, 16), 0),
        ((0, 0, 0), (0, 0), (16, 16), 3),
        ((199, 44, 58), (0, 16), (16, 16), 0),
        ((0, 0, 0), (0, 16), (16, 16), 3),
        ((138, 151, 71), (16, 16), (16, 16), 0),
        ((0, 0, 0), (16, 16), (16, 16), 3),
        ((138, 151, 71), (16, 32), (16, 16), 0),
        ((0, 0, 0), (16, 32), (16, 16), 3),
        ((199, 44, 58), (0, 32), (16, 16), 0),
        ((0, 0, 0), (0, 32), (16, 16), 3),
        ((199, 44, 58), (0, 48), (16, 16), 0),
        ((0, 0, 0), (0, 48), (16, 16), 3),
        ((1, 128, 181), (16, 48), (16, 16), 0),
        ((0, 0, 0), (16, 48), (16, 16), 3),
        ((1, 128, 181), (48, 32), (16, 16), 0),
        ((0, 0, 0), (48, 32), (16, 16), 3),
        ((138, 151, 71), (32, 32), (16, 16), 0),
        ((0, 0, 0), (32, 32), (16, 16), 3),
        ((199, 44, 58), (32, 48), (16, 16), 0),
        ((0, 0, 0), (32, 48), (16, 16), 3),
        ((138, 151, 71), (48, 48), (16, 16), 0),
        ((0, 0, 0), (48, 48), (16, 16), 3)}

    actual_rectangles = set(block.rectangles_to_draw())

    assert actual_rectangles.difference(expected_rectangles) == set()
    assert actual_rectangles.union(expected_rectangles) == expected_rectangles


def test_get_selected_block():
    """Test the selection process for getting individual blocks out of the board

    - Given a location and level, return correct part of the tree
    - Ensure that if the selection level is too deep or too shallow,
      a block is still returned
    """
    board, _ = construct_board()
    board.update_block_locations((0, 0), 50)

    assert equal_boards(board.children[0].children[0],
                        board.get_selected_block((40, 10), 2))
    assert equal_boards(board.children[0],
                        board.get_selected_block((40, 10), 1))
    assert equal_boards(board,
                        board.get_selected_block((40, 10), 0))

    # Always needs to return a block
    assert board.get_selected_block((100, 100), 0) is not None
    assert board.get_selected_block((-10, -10), 0) is not None
    assert board.get_selected_block((10, 100), 0) is not None
    assert board.get_selected_block((100, 10), 0) is not None


def test_swap():
    """Test the swapping of blocks in the tree.

    - Test against all of the standard boards, at different levels
    - Ensure the board changes when one swap is performed
    - Ensure that doing the same swap twice results in the original board
    """
    # A board to mutate.
    board, _ = construct_board()
    # A board to store the expected result.
    ans_board, _ = construct_board()
    # Another copy of the original board to compare against once we have
    # mutated board.
    ref_board, _ = construct_board()

    # Swap one direction and check resulting board
    board.swap(0)
    # By hand, make ans_board hold the correct answer.
    ans_board.children = [
        ans_board.children[1],
        ans_board.children[0],
        ans_board.children[3],
        ans_board.children[2]
    ]
    assert equal_boards(board, ans_board),\
        'Swapping does not match the reference configuration'

    # Swap the same direction again and ensure the operation is undone
    board.swap(0)
    assert equal_boards(board, ref_board),\
        'Performing same swap twice does not undo the operation'


def test_rotate():
    """Test the rotating of blocks in the tree

    - Test against all of the standard boards
    - Ensure the board changes when one rotation is performed
    - Ensure that doing opposite rotations results in the original board
    """
    board, _ = construct_board()
    # The board to modify
    ans_board, _ = construct_board()
    # What the tree should look like
    ref_board, _ = construct_board()

    # Rotate one of the children manually
    ans_board.children[0].children = [
        ans_board.children[0].children[1],
        ans_board.children[0].children[2],
        ans_board.children[0].children[3],
        ans_board.children[0].children[0]
    ]

    # Rotate one direction and check resulting board
    board.children[0].rotate(1)
    assert equal_boards(board, ans_board)
    # Rotate the opposite direction and ensure the operation is undone
    board.children[0].rotate(3)
    assert equal_boards(board, ref_board)


def test_smash():
    """Test to see if the block's children change after the smash operation.

    - Confirm that smashing has no effect where it is not allowed (at root
      node or at the max_depth)
    - This operation is random, so cannot
      check for an exact result, only whether the block state has changed
    """
    board, _ = construct_board()

    # What the tree should look like
    ref_board, _ = construct_board()

    # Cannot smash on the root block
    board.smash()
    assert equal_boards(board, ref_board)

    # Cannot smash on leaf block
    board.children[0].children[0].smash()
    assert equal_boards(board, ref_board)

    # Smash another block
    board.children[0].smash()
    assert not equal_boards(board, ref_board),\
        'A legal smash changed nothing; unlikely, but not necessarily an error'

def test_blob_goal():
    """Test the blob goal for the given board
    """
    board, _ = construct_board()

    # On the hand-constructed board, these are the correct scores for
    # each colour.
    correct_scores = [
        (COLOUR_LIST[0], 1),
        (COLOUR_LIST[1], 4),
        (COLOUR_LIST[2], 4),
        (COLOUR_LIST[3], 5)
    ]

    # Set up a goal for each colour and check results.
    for colour, score in correct_scores:
        goal = BlobGoal(colour)
        assert goal.score(board) == score


def test_perimeter_goal():
    """
    Test the blob goal for the given board
    """
    board, _ = construct_board()

    # On the hand-constructed board, these are the correct scores for
    # each colour.
    correct_scores = [
        (COLOUR_LIST[0], 2),
        (COLOUR_LIST[1], 5),
        (COLOUR_LIST[2], 4),
        (COLOUR_LIST[3], 5)
    ]

    # Set up a goal for each colour and check results.
    for colour, score in correct_scores:
        goal = PerimeterGoal(colour)
        assert goal.score(board) == score


def test_random_player_game():
    """
    Put 3 random players against each other and ensure the game ends
    """
    import random
    random.seed(1001)
    game = Game(4, 0, 3, [])
    game.run_game(3)


def test_smart_player_game():
    """
    Put 3 smart players against each other and ensure the game ends
    """
    import random
    random.seed(1001)
    game = Game(4, 0, 0, [1, 3, 5])
    game.run_game(3)


###############################################################################
# Test helpers
###############################################################################
def equal_boards(b1: Block, b2: Block) -> bool:
    """Return whether two blocks are equal, considering only structure and
    colours.
    """
    if len(b1.children) != len(b2.children):
        return False
    elif len(b1.children) == 0:
        return b1.colour == b2.colour
    else:
        for i in range(len(b1.children)):
            if not equal_boards(b1.children[i], b2.children[i]):
                return False
        return True


def construct_board() -> Tuple[Block, List[List[Tuple[int, int, int]]]]:
    """Return a fixed board and its flattened representation.
    """
    rootblock = Block(0, children=[
        Block(1, children=[
            Block(2, colour=COLOUR_LIST[0]),
            Block(2, colour=COLOUR_LIST[1]),
            Block(2, colour=COLOUR_LIST[1]),
            Block(2, colour=COLOUR_LIST[3])
        ]),
        Block(1, colour=COLOUR_LIST[2]),
        Block(1, colour=COLOUR_LIST[1]),
        Block(1, colour=COLOUR_LIST[3])
    ])

    rootblock.max_depth = 2

    # As we know the depth of the tree, we can set this depth per node
    for c in rootblock.children:
        c.max_depth = 2
        if len(c.children) > 0:
            for cc in c.children:
                cc.max_depth = 2

    flattened_block = [
        [COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[1]],
        [COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[1]],
        [COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[3], COLOUR_LIST[3]],
        [COLOUR_LIST[0], COLOUR_LIST[3], COLOUR_LIST[3], COLOUR_LIST[3]]
    ]

    return rootblock, flattened_block


if __name__ == '__main__':
    import pytest
    pytest.main(['simple_test.py'])
