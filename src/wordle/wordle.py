import os
from enum import Enum

import appdirs
import requests


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
    WORD_LIST_URL = "https://gist.githubusercontent.com/dracos/dd0668f281e685bad51479e5acaadb93/raw/6bfa15d263d6d5b63840a8e5b64e04b382fdb079/valid-wordle-words.txt"
    CACHE_DIR = appdirs.user_cache_dir("wordle-python", "wordle-python")
    WORD_LIST_FILE = os.path.join(CACHE_DIR, "valid-wordle-words.txt")

    def __init__(self, word: str, turns: int = 6):
        if len(word) != 5:
            raise ValueError("Word must be 5 letters long")
        self.word = word
        self.turns = turns
        self.guesses: list[Guess] = []
        self.valid_words = self._load_valid_words()
        if self.word not in self.valid_words:
            raise ValueError("Word is not in the valid word list")

    def _load_valid_words(self) -> set[str]:
        if not os.path.exists(self.WORD_LIST_FILE):
            os.makedirs(self.CACHE_DIR, exist_ok=True)
            response = requests.get(self.WORD_LIST_URL)
            response.raise_for_status()
            with open(self.WORD_LIST_FILE, "w") as f:
                f.write(response.text)
        with open(self.WORD_LIST_FILE) as f:
            return {line.strip() for line in f}

    def guess_word(self, guess_word: str) -> Guess:
        if len(guess_word) != 5:
            raise ValueError("Guess must be 5 letters long")
        if len(self.guesses) >= self.turns:
            raise Exception("No more turns left")
        if guess_word not in self.valid_words:
            raise ValueError("Not a valid word")
        guess = Guess(guess_word, self.word)
        self.guesses.append(guess)
        return guess
