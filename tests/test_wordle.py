import pytest
from wordle.wordle import Wordle, LetterColor


def test_wordle_init():
    game = Wordle("apple")
    assert game.word == "apple"
    assert game.turns == 6


def test_wordle_init_invalid_word():
    with pytest.raises(ValueError):
        Wordle("banana")


def test_guess_word():
    game = Wordle("apple")
    guess = game.guess_word("apply")
    assert len(game.guesses) == 1
    assert guess.word == "apply"
    assert guess.colors == [
        LetterColor.GREEN,
        LetterColor.GREEN,
        LetterColor.GREEN,
        LetterColor.GREEN,
        LetterColor.GRAY,
    ]


def test_guess_word_invalid_length():
    game = Wordle("apple")
    with pytest.raises(ValueError):
        game.guess_word("banana")


def test_guess_word_no_more_turns():
    game = Wordle("apple", turns=1)
    game.guess_word("apply")
    with pytest.raises(Exception):
        game.guess_word("apply")


def test_guess_all_gray():
    game = Wordle("apple")
    guess = game.guess_word("bbbbb")
    assert guess.colors == [
        LetterColor.GRAY,
        LetterColor.GRAY,
        LetterColor.GRAY,
        LetterColor.GRAY,
        LetterColor.GRAY,
    ]


def test_guess_all_yellow():
    game = Wordle("apple")
    guess = game.guess_word("elppa")
    assert guess.colors == [
        LetterColor.YELLOW,
        LetterColor.YELLOW,
        LetterColor.GREEN,
        LetterColor.YELLOW,
        LetterColor.YELLOW,
    ]


def test_guess_all_green():
    game = Wordle("apple")
    guess = game.guess_word("apple")
    assert guess.colors == [
        LetterColor.GREEN,
        LetterColor.GREEN,
        LetterColor.GREEN,
        LetterColor.GREEN,
        LetterColor.GREEN,
    ]


def test_challenging_guess():
    game = Wordle("tapes")
    guess = game.guess_word("guess")
    assert guess.colors == [
        LetterColor.GRAY,
        LetterColor.GRAY,
        LetterColor.YELLOW,
        LetterColor.GRAY,
        LetterColor.GREEN,
    ]


def test_duplicate_letters_in_guess():
    game = Wordle("speed")
    guess = game.guess_word("deeds")
    assert guess.colors == [
        LetterColor.YELLOW,
        LetterColor.YELLOW,
        LetterColor.GREEN,
        LetterColor.GRAY,
        LetterColor.YELLOW,
    ]
