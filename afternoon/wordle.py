import random
import requests

class Wordle:
    def __init__(self, word_list):
        self.word_list = word_list
        self.secret_word = random.choice(self.word_list)
        self.attempts = 6
        self.guesses = []

    def guess(self, word):
        if len(word) != 5:
            return "Guess must be 5 letters long."
        if word not in self.word_list:
            return "Not a valid word."

        self.attempts -= 1
        self.guesses.append(word)

        feedback = []
        for i in range(5):
            if word[i] == self.secret_word[i]:
                feedback.append("Green")
            elif word[i] in self.secret_word:
                feedback.append("Yellow")
            else:
                feedback.append("Gray")
        return feedback

    def is_game_over(self):
        return self.attempts == 0 or (len(self.guesses) > 0 and self.guesses[-1] == self.secret_word)

class WordleSolver:
    def __init__(self, word_list):
        self.word_list = word_list
        self.possible_words = self.word_list[:]

    def solve(self, game):
        while not game.is_game_over():
            best_guess = self.choose_best_guess()
            print(f"Solver guesses: {best_guess}")
            feedback = game.guess(best_guess)
            print(f"Feedback: {feedback}")
            self.filter_word_list(best_guess, feedback)
            if best_guess == game.secret_word:
                print("Solver found the word!")
                return

    def choose_best_guess(self):
        if not self.possible_words:
            return random.choice(self.word_list)
        return self.possible_words[0]

    def filter_word_list(self, guess, feedback):
        new_possible_words = []
        for word in self.possible_words:
            if self.is_word_possible(word, guess, feedback):
                new_possible_words.append(word)
        self.possible_words = new_possible_words

    def is_word_possible(self, word, guess, feedback):
        for i in range(5):
            if feedback[i] == "Green" and word[i] != guess[i]:
                return False
            elif feedback[i] == "Yellow":
                if word[i] == guess[i] or guess[i] not in word:
                    return False
            elif feedback[i] == "Gray" and guess[i] in word:
                # Handle duplicate letters correctly
                if word.count(guess[i]) != guess[:i].count(guess[i]):
                    return False
        return True
def load_word_list_from_url(url):
    """Loads a word list from a URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4XX or 5XX)
        
        # Decode content to string, split into lines, and filter for 5-letter words
        words = [word.lower() for word in response.text.splitlines() if len(word) == 5]
        with open("word_list.txt", "w") as file:
            file.write("\n".join(words))
        return words
    except requests.exceptions.RequestException as e:
        print(f"Error fetching word list from URL: {e}")
        return []
 
def main():
    word_list_url = "https://raw.githubusercontent.com/charlesreid1/five-letter-words/master/sgb-words.txt"
    word_list = load_word_list_from_url(word_list_url)
    if not word_list:
        return # Exit if the word list couldn't be loaded
 
    game = Wordle(word_list)
    solver = WordleSolver(word_list)

    print("Welcome to Wordle!")
    print(f"The secret word has 5 letters. You have {game.attempts} attempts.")

    # Uncomment the line below to let the solver play
    solver.solve(game)

    # Comment out the following loop if you want the solver to play
    while not game.is_game_over():
        try:
            player_guess = input("Enter your guess: ").lower()
            feedback = game.guess(player_guess)
            print(f"Feedback: {feedback}")
            if player_guess == game.secret_word:
                print(f"Congratulations! You guessed the word in {6 - game.attempts} attempts.")
                break
        except TypeError as e:
            print(e)
    else:
        if game.attempts == 0:
            print(f"Game over! The word was {game.secret_word}")

if __name__ == "__main__":
    main()
