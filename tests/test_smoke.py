from rltetris import _core

def test_engine_smoke_returns_a_valid_block_type():
    assert 0 <= _core.engine_smoke(1) <= 6


def test_engine_smoke_same_seed_gives_same_piece():
    assert _core.engine_smoke(42) == _core.engine_smoke(42)


def test_engine_smoke_different_seeds_vary_the_piece():
    pieces = {_core.engine_smoke(seed) for seed in range(50)}
    assert len(pieces) > 1
