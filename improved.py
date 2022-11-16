"""
I pledge on my honor that I have not given or received
any unauthorized assistance on this project.
Manu Madhu Pillai
"""

import random
import math
from reversi import getBoardCopy, makeMove, getValidMoves, getScoreOfBoard

seen_state = []
rewards = {}
tries = {}
my_tile = []
prev_board = []


def ucb_choose(board, tile, exploration_param):
    """
    Returns a move chosen based on Upper Confidence Bound Algorithm.

            Parameters:
                board(list): Game Board
                tile(string): denotes the current player's turn
            Returns:
                tuple: Move chosen by UCB algorithm
    """

    dupe_board = getBoardCopy(board)
    possible_moves = getValidMoves(board, tile)
    random.shuffle(possible_moves)
    tiles = ["X", "O"]
    # Finding opponent tile for Game
    if my_tile == tiles[0]:
        comp_tile = tiles[1]
    else:
        comp_tile = tiles[0]

    for child in possible_moves:
        makeMove(dupe_board, tile, child[0], child[1])
        if (dupe_board, tile) not in seen_state:
            return (dupe_board, tile)
            # Randomly choose one of unseen valid moves

    # No unseen moves left, selecting move with highest UCB
    dupe_board = getBoardCopy(board)
    q_max = -math.inf
    sum_tries = 0

    for child in possible_moves:
        makeMove(dupe_board, tile, child[1], child[2])
        sum_tries += tries[(str(dupe_board), tile)]
        dupe_board = getBoardCopy(board)

    if tile == my_tile:  # Max node
        for child in possible_moves:
            makeMove(dupe_board, tile, child[0], child[1])
            q_value = rewards[(str(dupe_board), tile)] / tries[
                (str(dupe_board), tile)
            ] + exploration_param * math.sqrt(
                math.log(sum_tries) / tries[(str(dupe_board), tile)]
            )
            if q_value > q_max:
                q_max = q_value
                selected_move = (dupe_board, tile)
            dupe_board = getBoardCopy(board)
    else:  # Min Node
        for child in possible_moves:
            makeMove(dupe_board, tile, child[0], child[1])
            # Q value from UCB formula
            q_value = (1 - rewards[(str(dupe_board), tile)]) / tries[
                (str(dupe_board), tile)
            ] + exploration_param * math.sqrt(
                math.log(sum_tries) / tries[(str(dupe_board), tile)]
            )
            # Inner score reward function to encourage play towards the center of the board
            inner_score = (
                0.7
                * q_value
                / math.sqrt(math.pow(child[0] - 3.5, 2) + math.pow(child[1] - 3.5, 2))
            )

            q_value = (
                q_value
                + inner_score
                - get_greedy_penalty(1.5, dupe_board, comp_tile)
                - calc_position_penalty(child, 0.7, 0.5, q_value)
            )
            if q_value > q_max:
                q_max = q_value
                selected_move = (dupe_board, tile)
    return selected_move[0], selected_move[1]


def get_greedy_penalty(greedy_wt, dupe_board, comp_tile):
    """
    Penalty function to discourage flipping of tiles early in the game which
    reduces available turns in the next moves.
            Parameters:
               greedy_wt(float): penalty weight for early flipping of tiles.
               dupe_board(list): game board
               comp_tile(string): competitor's tile.
           Returns:
               float: penalty value

    """
    greedy_penalty = (
        getScoreOfBoard(dupe_board)[comp_tile] - getScoreOfBoard(dupe_board)[my_tile]
    ) / math.pow(
        (getScoreOfBoard(dupe_board)[comp_tile] + getScoreOfBoard(dupe_board)[my_tile]),
        greedy_wt,
    )
    return greedy_penalty


def calc_position_penalty(child, diag_wt, edge_wt, q_value):
    """
    Returns a penalty for bad positions that can lead to corner capturing.

           Parameters:
               child(list): positions of available moves after a move is made.
               diag_wt(float): penalty weight for diagnoal to corner location
               edge_wt(float): penalty weight for edge to corner location
           Returns:
               float: penalty value
    """
    if child[0] == 0:
        if child[1] == 1 or child[1] == 6:
            position_penalty = edge_wt * q_value
        elif child[0] == 1:
            if child[1] == 7 or child[1] == 0:
                position_penalty = edge_wt * q_value
            else:
                position_penalty = diag_wt * q_value
        elif child[0] == 6:
            if child[1] == 7 or child[1] == 0:
                position_penalty = edge_wt * q_value
            else:
                position_penalty = diag_wt * q_value
        elif child[0] == 7:
            if child[1] == 1 or child[1] == 6:
                position_penalty = edge_wt * q_value
    return position_penalty


def uct(board, tile, exploration_param):
    """
    Returns a preference value for a move based on UCB for Trees Algorithm.

            Parameters:
                board(list): Game Board
                tile(string): denotes the current player's turn
            Returns:
                float: preference value
    """

    value = 0
    board_backup = getBoardCopy(board)
    tile_backup = tile

    # Check  if move was seen before
    if (board_backup, tile_backup) not in seen_state:
        seen_state.append((board_backup, tile_backup))
        tries[(str(board_backup), tile_backup)] = 0
        rewards[(str(board_backup), tile_backup)] = 0

    tiles = ["X", "O"]
    # Finding opponent tile for UCT
    if tile == tiles[0]:
        opp_tile = tiles[1]
    else:
        opp_tile = tiles[0]
    # Finding opponent tile for Game
    if my_tile == tiles[0]:
        comp_tile = tiles[1]
    else:
        comp_tile = tiles[0]

    dupe_board = getBoardCopy(board)
    if getValidMoves(dupe_board, tile) == []:
        # Terminal Node
        value = (
            getScoreOfBoard(dupe_board)[my_tile]
            - getScoreOfBoard(dupe_board)[comp_tile]
        )
        if value > 0:  # win
            value = 1
        else:
            value = 0  # loss
    else:
        updated_board, _ = ucb_choose(board, tile, exploration_param)
        value = uct(updated_board, opp_tile, exploration_param)

    rewards[(str(board_backup), tile_backup)] = (
        rewards[(str(board_backup), tile_backup)]
        * tries[(str(board_backup), tile_backup)]
        + value
    ) / (tries[(str(board_backup), tile_backup)] + 1)

    # Normalize Rewards
    if (max(rewards.values()) - min(rewards.values())) != 0:
        normalizer = max(rewards.values()) - min(rewards.values())
        for key in rewards:
            rewards[key] = rewards[key] - min(rewards.values()) / normalizer
    tries[(str(board_backup), tile_backup)] += 1
    return value


def get_move(board, tile):
    """
    Returns a move based on UCB for Trees Algorithm.

            Parameters:
                board(list): Game Board
                tile(string): denotes the current player's turn

            Returns:
                list: Selected Move of the current player.
    """
    if "my_tile" not in globals():
        # Initialization
        global my_tile
        global seen_state
        global rewards
        global tries
        global prev_board

        my_tile = tile
        seen_state = []
        rewards = {}
        tries = {}
        prev_board = getBoardCopy(board)

    if prev_board != board:
        # Flush old values
        my_tile = tile
        seen_state = []
        rewards = {}
        tries = {}

    uct(board, tile, math.sqrt(2))

    possible_moves = getValidMoves(board, tile)
    random.shuffle(possible_moves)
    # Randomizing move order

    q_max = -math.inf
    dupe_board = getBoardCopy(board)
    selected_move = None

    tiles = ["X", "O"]
    if tile == tiles[0]:
        opponent_tile = tiles[1]
    else:
        opponent_tile = tiles[0]

    for move in possible_moves:
        makeMove(dupe_board, tile, move[0], move[1])
        if (str(dupe_board), opponent_tile) in rewards.keys():
            if rewards[(str(dupe_board), opponent_tile)] > q_max:
                q_max = rewards[(str(dupe_board), opponent_tile)]
                selected_move = move
        dupe_board = getBoardCopy(board)

    prev_board = getBoardCopy(board)
    # Saving board state to determine flushing global variable values
    return selected_move
