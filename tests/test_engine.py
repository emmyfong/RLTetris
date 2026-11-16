import numpy as np

from rltetris import Action, BlockType, Engine


def piece_sequence(seed, count=7):
    """The first `count` pieces of a game, hard-dropping each in the spawn column."""
    engine = Engine(seed)
    sequence = [engine.current_block.type]
    for _ in range(count - 1):
        engine.step(Action.HardDrop)
        sequence.append(engine.current_block.type)
    return sequence


def test_new_engine_starts_in_a_fresh_state():
    engine = Engine(1)
    assert engine.score == 0
    assert engine.level == 1
    assert engine.game_over is False


def test_ghost_row_is_below_the_spawn_row_and_on_the_board():
    engine = Engine(1)
    assert engine.current_block.row < engine.ghost_row <= 19


def test_move_left_shifts_piece_one_column():
    engine = Engine(7)
    start_col = engine.current_block.col
    engine.step(Action.MoveLeft)
    assert engine.current_block.col == start_col - 1


def test_move_left_stops_at_the_left_wall():
    engine = Engine(7)
    for _ in range(20):
        engine.step(Action.MoveLeft)
    assert engine.current_block.col == 0


def test_hold_stores_current_piece_and_promotes_next():
    engine = Engine(5)
    assert engine.hold_block is None
    first = engine.current_block.type
    upcoming = engine.next_block.type
    engine.step(Action.Hold)
    assert engine.hold_block.type == first
    assert engine.current_block.type == upcoming


def test_same_seed_gives_same_piece_sequence():
    assert piece_sequence(42) == piece_sequence(42)


def test_different_seeds_give_different_piece_sequences():
    sequences = {tuple(piece_sequence(seed)) for seed in range(20)}
    assert len(sequences) > 1


def test_first_seven_pieces_are_one_of_each_type():
    for seed in range(5):
        assert len(set(piece_sequence(seed))) == 7


def test_new_engine_has_an_empty_20_by_10_grid():
    grid = Engine(1).grid
    assert grid.shape == (20, 10)
    assert grid.dtype == np.uint8
    assert not grid.any()


def test_hard_drop_locks_four_cells_and_promotes_next_piece():
    engine = Engine(7)
    dropped = engine.current_block.type
    upcoming = engine.next_block.type
    engine.step(Action.HardDrop)
    filled = engine.grid[engine.grid != 0]
    assert len(filled) == 4
    assert (filled == dropped.value + 1).all()
    assert engine.current_block.type == upcoming


def test_grid_is_a_copy_not_a_view_of_engine_memory():
    engine = Engine(7)
    snapshot = engine.grid
    engine.step(Action.HardDrop)
    assert not snapshot.any()


def test_same_seed_and_actions_give_identical_grids():
    script = [Action.MoveLeft, Action.Rotate, Action.HardDrop] * 6

    def play(seed):
        engine = Engine(seed)
        for action in script:
            engine.step(action)
        return engine

    first, second = play(11), play(11)
    assert np.array_equal(first.grid, second.grid)
    assert first.score == second.score
    assert first.current_block.type == second.current_block.type


def test_stacking_in_the_spawn_column_ends_the_game_and_freezes_it():
    engine = Engine(3)
    for _ in range(40):
        engine.step(Action.HardDrop)
        if engine.game_over:
            break
    assert engine.game_over

    frozen = engine.grid
    engine.step(Action.HardDrop)
    engine.step(Action.MoveLeft)
    assert np.array_equal(engine.grid, frozen)
