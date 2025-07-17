import pytest
from unittest.mock import patch, mock_open
from wordle.wordle import Wordle, LetterColor

VALID_WORDS = {"apple", "apply", "tapes", "guess", "speed", "deeds", "zesty", "pleat", "fjord"}

@pytest.fixture
def mock_word_list(mocker):
    """Fixture to mock the word list loading mechanism."""
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("builtins.open", mock_open(read_data="\n".join(VALID_WORDS)))
    # Prevent actual network requests in tests that might miss the mock
    mocker.patch("requests.get")


def test_wordle_init(mock_word_list):
    game = Wordle("apple")
    assert game.word == "apple"
    assert game.turns == 6
    assert "apple" in game.valid_words


def test_wordle_init_invalid_word_length():
    with pytest.raises(ValueError, match="Word must be 5 letters long"):
        Wordle("banana")


def test_wordle_init_word_not_in_list(mock_word_list):
    with pytest.raises(ValueError, match="Word is not in the valid word list"):
        Wordle("zzzzz")


def test_guess_word(mock_word_list):
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


def test_guess_word_not_in_list(mock_word_list):
    game = Wordle("apple")
    with pytest.raises(ValueError, match="Not a valid word"):
        game.guess_word("bbbbb")


def test_guess_word_invalid_length(mock_word_list):
    game = Wordle("apple")
    with pytest.raises(ValueError, match="Guess must be 5 letters long"):
        game.guess_word("banana")


def test_guess_word_no_more_turns(mock_word_list):
    game = Wordle("apple", turns=1)
    game.guess_word("apply")
    with pytest.raises(Exception, match="No more turns left"):
        game.guess_word("apply")


def test_guess_all_gray(mock_word_list):
    game = Wordle("apple")
    guess = game.guess_word("fjord")
    assert guess.colors == [
        LetterColor.GRAY,
        LetterColor.GRAY,
        LetterColor.GRAY,
        LetterColor.GRAY,
        LetterColor.GRAY,
    ]


def test_guess_all_yellow(mock_word_list):
    game = Wordle("apple")
    guess = game.guess_word("pleat")
    assert guess.colors == [
        LetterColor.YELLOW,
        LetterColor.YELLOW,
        LetterColor.YELLOW,
        LetterColor.YELLOW,
        LetterColor.GRAY,
    ]


def test_guess_all_green(mock_word_list):
    game = Wordle("apple")
    guess = game.guess_word("apple")
    assert guess.colors == [
        LetterColor.GREEN,
        LetterColor.GREEN,
        LetterColor.GREEN,
        LetterColor.GREEN,
        LetterColor.GREEN,
    ]


def test_challenging_guess(mock_word_list):
    game = Wordle("tapes")
    guess = game.guess_word("guess")
    assert guess.colors == [
        LetterColor.GRAY,
        LetterColor.GRAY,
        LetterColor.YELLOW,
        LetterColor.GRAY,
        LetterColor.GREEN,
    ]


def test_duplicate_letters_in_guess(mock_word_list):
    game = Wordle("speed")
    guess = game.guess_word("deeds")
    assert guess.colors == [
        LetterColor.YELLOW,
        LetterColor.YELLOW,
        LetterColor.GREEN,
        LetterColor.GRAY,
        LetterColor.YELLOW,
    ]

def test_word_list_download(mocker):
    """Test that the word list is downloaded if it doesn't exist."""
    mocker.patch("os.path.exists", return_value=False)
    mocker.patch("os.makedirs")

    mock_file_content = "apple\napply"
    # Separate mocks for write and read
    mock_write = mock_open()
    mock_read = mock_open(read_data=mock_file_content)

    # Use a lambda to switch between mocks
    mocker.patch("builtins.open", lambda f, mode='r': mock_write.return_value if mode == 'w' else mock_read.return_value)

    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.text = mock_file_content
    mock_response.raise_for_status = mocker.Mock()
    mocker.patch("requests.get", return_value=mock_response)

    game = Wordle("apple")

    assert game.valid_words == {"apple", "apply"}
    mock_write().write.assert_called_once_with(mock_file_content)
