import inspect
import os
import random
import importlib
import time

import pytablewriter
import numpy as np
from pytablewriter.style import Style

from WordList import *
from WordleAI import *
#from ai_implementations import LetterPopularityAI
from ai_implementations import simoniiAI

class Competition:

    def __init__(self, competitor_directory, wordlist_filename="data/official/combined_wordlist.txt", hard_mode=False):
        self.competitor_directory = competitor_directory
        self.wordlist = WordList(wordlist_filename)
        self.words = self.wordlist.get_list_copy()
        self.competitors = self.load_competitors()
        self.hard_mode = hard_mode

    def load_competitors(self):
        competitors = []
        for file in os.listdir(self.competitor_directory):
            if file.endswith(".py"):
                module = importlib.import_module(self.competitor_directory + "." + file[:-3])
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and issubclass(obj, WordleAI) and not inspect.isabstract(obj):
                        competitors.append(obj(self.wordlist.get_list_copy()))

        return competitors

    def guess_is_legal(self, guess, guess_history):
        return len(guess) == 5 and guess.lower() == guess and guess in self.words and (
                not self.hard_mode or is_hard_mode(guess, guess_history))

    def play(self, competitor, word):
        guesses = []
        success = False
        guess_history = []

        for i in range(20):  # Up to 6 guesses
            guess = competitor.guess(guess_history)
            if not self.guess_is_legal(guess, guess_history):
                print("Competitor ", competitor.__class__.__name__, " is a dirty cheater!")
                print("hard_mode: ", self.hard_mode, "guess: ", guess, "guess_history", guess_history)
                print("Competition aborted.")
                quit()
            
            peg = self.ternaryToKey(self.check_peg(guess, word))
            
            guess_result = []
            for c in range(5):
                if peg[c] == "n":
                    guess_result.append(LetterInformation.NOT_PRESENT)
                elif peg[c] == "c":
                    guess_result.append(LetterInformation.CORRECT)
                else:
                    guess_result.append(LetterInformation.PRESENT)
            guess_history.append((guess, guess_result))
            guesses.append(guess)

            if guess == word:
                if i <6:
                    success = True
                break
        return success, guesses
    
    def check_peg(self, guess, word):
        flagi= [bool(1),bool(1),bool(1),bool(1),bool(1)]  #'true = need to be checked'
        flagj= [bool(1),bool(1),bool(1),bool(1),bool(1)]  #'true = need to be checked'
        peg=0
        for i in range(5):
            if(guess[i]==word[i]):
                peg += 2 *(100000/(10**(i+1)))
                flagi[i]=bool(0)
                flagj[i]=bool(0)
        for i in range(5):
            for j in range(5):
                if flagi[i]:
                    if flagj[j]:
                        if guess[i]==word[j]:
                            peg += 100000/(10**(i+1))
                            flagi[i]=bool(0)
                            flagj[j]=bool(0)
                            j=6
        return peg
    def ternaryToKey(self, peg):
        myString = str()
        for i in range(5):
            q, mod = divmod(peg, 10**(4-i))
            peg = mod
            if (q == 2):
                myString= myString + "c"
            elif (q == 1):
                myString= myString + "p"
            else:
                myString= myString + "n"
        return myString
      
    
    def fight(self, rounds, print_details=False, solution_wordlist_filename='data/official/combined_wordlist.txt',
              shuffle=False):
        print("Start tournament")
        result = {}
        success_total = {}
        guesses = {}
        points = {}
        round_words = []

        for competitor in self.competitors:
            result[competitor] = 0
            success_total[competitor] = 0
            guesses[competitor] = []
            points[competitor] = []
        fight_words = WordList(solution_wordlist_filename).get_list_copy()
        start = time.time()
        competitor_times = np.zeros(len(self.competitors))
        with open('allTrial.txt', 'w') as f :
            for r in range(rounds):
                word = random.choice(fight_words) if shuffle else fight_words[r]
                current_time = time.time() - start
                round_words.append(word)
                c = 0
                for competitor in self.competitors:
                    #print("\rRound", r + 1, "/", rounds, "word =", word, "competitior", c + 1, "/", len(self.competitors),
                    #      "time", current_time, "/", current_time * rounds / (r + 1), end='')
                    competitor_start = time.time()
                    success, round_guesses = self.play(competitor, word)
                    round_points = len(round_guesses) if success else 10
                    result[competitor] += round_points
                    guesses[competitor].append(round_guesses)
                    points[competitor].append(round_points)
                    if success:
                        success_total[competitor] += 1
                    competitor_times[c] += time.time() - competitor_start
                    c += 1
                    f.write(str(word))
                    f.write("\t")
                    f.write(str(round_points))
                    f.write("\t")
                    f.write(str(round_guesses))
                    f.write('\n')

        print("\n")
        for i in range(len(competitor_times)):
            print(self.competitors[i].__class__.__name__, "calculation took", "{:.3f}".format(competitor_times[i]), "seconds")

        print("")
        if print_details:
            print("Words: ", round_words)
            print("Guesses: ", guesses)
            print("Points per round: ", points)
            print("")

        print("Competition finished with ", rounds, " rounds, ", len(self.competitors), " competitors and hard_mode = ", self.hard_mode,"\n")
        result = dict(sorted(result.items(), key=lambda item: item[1]))

        writer = pytablewriter.MarkdownTableWriter()
        writer.table_name = "Leaderboard"
        writer.headers = ["Nr", "AI", "Author", "Points per round", "Success rate"]
        for i in range(len(writer.headers)):
            writer.set_style(column=i, style=Style(align="left"))
        writer.value_matrix = []

        placement = 1
        for competitor in result:
            writer.value_matrix.append(
                [placement, competitor.__class__.__name__, competitor.get_author(), result[competitor] / rounds,
                 str(100 * success_total[competitor] / rounds) + "%"])
            placement += 1
        writer.write_table()


def is_hard_mode(word, guess_history):
    """
    Returns True if the word is a legal guess in hard mode.
    """
    return len(LetterPopularityAI.remaining_options([word], guess_history)) == 1


def main():
    np.set_printoptions(threshold=np.inf)
    np.set_printoptions(suppress=True)

    competition = Competition("simoniiAI", wordlist_filename="data/official/combined_wordlist.txt", hard_mode=False)
    competition.fight(rounds=12972, solution_wordlist_filename="data/official/combined_wordlist.txt", print_details=False)
    #competition.fight(rounds=10, solution_wordlist_filename="data/official/shuffled_real_wordles.txt", print_details=False)

if __name__ == "__main__":
    main()
