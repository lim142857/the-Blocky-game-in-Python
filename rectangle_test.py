from block import Block
from renderer import COLOUR_LIST

def test_rectangles_to_draw():
    """
    Tests the rectangles to draw method.
    """
    # Compute the rectangles for this hard-coded example.
    # Convert to a set, since no particular rectangle order was required.
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
    block.update_block_locations((0, 0), 50)
    actual_set = set(block.rectangles_to_draw())

    # Define the correct set of rectangles, again as a set.
    correct_rectangles = [((138, 151, 71), (37, 0), (12, 12), 0),
                          ((0, 0, 0), (37, 0), (12, 12), 3),
                          ((199, 44, 58), (25, 0), (12, 12), 0),
                          ((0, 0, 0), (25, 0), (12, 12), 3),
                          ((138, 151, 71), (25, 12), (12, 12), 0),
                          ((0, 0, 0), (25, 12), (12, 12), 3),
                          ((1, 128, 181), (37, 12), (12, 12), 0),
                          ((0, 0, 0), (37, 12), (12, 12), 3),
                          ((1, 128, 181), (12, 0), (12, 12), 0),
                          ((0, 0, 0), (12, 0), (12, 12), 3),
                          ((199, 44, 58), (0, 0), (12, 12), 0),
                          ((0, 0, 0), (0, 0), (12, 12), 3),
                          ((199, 44, 58), (0, 12), (12, 12), 0),
                          ((0, 0, 0), (0, 12), (12, 12), 3),
                          ((138, 151, 71), (12, 12), (12, 12), 0),
                          ((0, 0, 0), (12, 12), (12, 12), 3),
                          ((138, 151, 71), (12, 25), (12, 12), 0),
                          ((0, 0, 0), (12, 25), (12, 12), 3),
                          ((199, 44, 58), (0, 25), (12, 12), 0),
                          ((0, 0, 0), (0, 25), (12, 12), 3),
                          ((199, 44, 58), (0, 37), (12, 12), 0),
                          ((0, 0, 0), (0, 37), (12, 12), 3),
                          ((1, 128, 181), (12, 37), (12, 12), 0),
                          ((0, 0, 0), (12, 37), (12, 12), 3),
                          ((1, 128, 181), (37, 25), (12, 12), 0),
                          ((0, 0, 0), (37, 25), (12, 12), 3),
                          ((138, 151, 71), (25, 25), (12, 12), 0),
                          ((0, 0, 0), (25, 25), (12, 12), 3),
                          ((199, 44, 58), (25, 37), (12, 12), 0),
                          ((0, 0, 0), (25, 37), (12, 12), 3),
                          ((138, 151, 71), (37, 37), (12, 12), 0),
                          ((0, 0, 0), (37, 37), (12, 12), 3)]
    correct_set = set(correct_rectangles)

    # There must be no difference between the actual set and the correct set!
    assert actual_set.difference(correct_set) == set()
    assert correct_set.difference(actual_set) == set()
