from enum import Enum


class LetterColor(Enum):
    GREEN = "green"
    YELLOW = "yellow"
    GRAY = "gray"


class Guess:
    def __init__(self, word: str, target_word: str):
        if len(word) != 5:
            raise ValueError("Guess must be 5 letters long")
        self.word = word
        self.target_word = target_word
        self.colors = self._calculate_colors()

    def _calculate_colors(self) -> list[LetterColor]:
        colors = [LetterColor.GRAY] * 5
        target_word_list = list(self.target_word)
        for i, letter in enumerate(self.word):
            if letter == target_word_list[i]:
                colors[i] = LetterColor.GREEN
                target_word_list[i] = None  # Mark as used

        for i, letter in enumerate(self.word):
            if colors[i] == LetterColor.GREEN:
                continue
            if letter in target_word_list:
                colors[i] = LetterColor.YELLOW
                target_word_list.remove(letter)  # Mark as used
        return colors


class Wordle:
    def __init__(self, word: str, turns: int = 6):
        if len(word) != 5:
            raise ValueError("Word must be 5 letters long")
        self.word = word
        self.turns = turns
        self.guesses: list[Guess] = []

    def guess_word(self, guess_word: str) -> Guess:
        if len(self.guesses) >= self.turns:
            raise Exception("No more turns left")
        guess = Guess(guess_word, self.word)
        self.guesses.append(guess)
        return guess
