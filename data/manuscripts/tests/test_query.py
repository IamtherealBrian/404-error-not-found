import data.manuscripts.query as mqry
import random
import pytest


def gen_random_not_valid_str()-> str:
    BIG_NUM = 10_000_000_000
    big_int = random.randint(0, BIG_NUM)
    big_int += BIG_NUM
    bad_str = str(big_int)


def test_is_valid_state():
    for state in mqry.get_states():
        assert mqry.is_valid_state(state)


def test_is_not_valid_state():
    for state in mqry.get_states():
        assert not mqry.is_valid_state(gen_random_not_valid_str)


def test_is_valid_action():
    for action in mqry.get_actions():
        assert mqry.is_valid_action(action)


def test_handle_action_bad_state():
    with pytest.raises(ValueError):
        mqry.handle_action(gen_random_not_valid_str(),
                           mqry.TEST_ACTION,
                           manu=mqry.SAMPLE_MANU)


def test_handle_action_bad_action():
    with pytest.raises(ValueError):
        mqry.handle_action(mqry.TEST_STATE,
                           gen_random_not_valid_str(),
                           manu=mqry.SAMPLE_MANU)


def test_handle_action_valid_return():
    for state in mqry.get_states():
        for action in mqry.get_valid_actions_by_state(state):
            print(f'{action=}')
            new_state = mqry.handle_action(state, action,
                                           manu=mqry.SAMPLE_MANU,
                                           ref='Some ref')
            print(f'{new_state=}')
            assert mqry.is_valid_state(new_state)