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
