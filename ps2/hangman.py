# Problem Set 2: Hangman
# Author: Mykyta Horovoi
# Collaborators: None

# Hangman Game
# -----------------------------------

import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    inFile = open(WORDLIST_FILENAME, 'r')
    line = inFile.readline()
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    return set(secret_word) & set(letters_guessed) == set(secret_word) 


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    guess = ""
    for char in secret_word:
        if char in letters_guessed:
            guess += char
        else:
            guess += "_ "
    return guess


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    return ''.join(sorted(set(string.ascii_lowercase) - set(letters_guessed)))
    

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    guesses_to_fail = 6
    flag = False
    letters_guessed = []
    warnings = 3

    print('Welcome to the game, Hangman!')
    print('I am thinking of a word that is ' + str(len(secret_word)) +' letters long.')
    print('You have ' + str(warnings) +' warnings left.')
    print("-----------")

    while flag == False:
        print('You have ' + str(guesses_to_fail)  + ' guesses left.')
        print('Available letters: ' + get_available_letters(letters_guessed))
        guess = input('Please guess a letter: ').lower()

        if guess not in (get_available_letters(letters_guessed) and string.ascii_lowercase) and warnings > 0:
            warnings -= 1
            print("Oops! That is not a valid letter.", "You have " + str(warnings) + " warnings left:", get_guessed_word(secret_word, letters_guessed))
            print("-----------")

        elif guess not in (get_available_letters(letters_guessed) and string.ascii_lowercase) and warnings <= 0:
            warnings -= 1
            print("Oops! That is not a valid letter.", "You have no warnings left so you lose one guess:", get_guessed_word(secret_word, letters_guessed))
            print("-----------")
            guesses_to_fail -= 1

        elif guess not in get_available_letters(letters_guessed) and warnings > 0:
            warnings -= 1
            print("Oops! You've already guessed that letter.", "You have " + str(warnings) + " warnings left:", get_guessed_word(secret_word, letters_guessed))
            print("-----------")

        elif guess not in get_available_letters(letters_guessed) and warnings <= 0:
            warnings -= 1
            print("Oops! You've already guessed that letter.", "You have no warnings left so you lose one guess:", get_guessed_word(secret_word, letters_guessed))
            print("-----------")
            guesses_to_fail -= 1

        elif guess in secret_word and get_available_letters(letters_guessed):
            letters_guessed += [guess]
            print('Good guess: ' + get_guessed_word(secret_word, letters_guessed))
            print("-----------")

        elif guess not in secret_word and get_available_letters(letters_guessed):
            print('Oops! That letter is not in my word: ' + get_guessed_word(secret_word, letters_guessed))
            print("-----------")
            letters_guessed += [guess]
            if guess in 'aeiou':
              guesses_to_fail -= 2
            else:
              guesses_to_fail -= 1

        if is_word_guessed(secret_word, letters_guessed) == True:
            flag = True
            print("Congratulations, you won!")
            print("Your total score for this game is: " + str(guesses_to_fail * len(set(secret_word))))

        elif guesses_to_fail == 0:
            flag = True
            print('Sorry, you ran out of guesses. The word was ' + secret_word + '.')

# -----------------------------------


def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
        other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol_ ,
        and my_word and other_word are of the same length; False otherwise: 
    '''
    my_word = my_word.replace(" ", "")
    if len(my_word) == len(other_word):
        for i in range(len(my_word)):
            if my_word[i] != "_" and my_word[i] != other_word[i]:
                return False
            elif my_word[i] == "_" and other_word[i] in my_word:
                return False
        return True
    else:
      return False


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.
    '''
    list = []
    for word in wordlist:
        if match_with_gaps(my_word, word):
            list.append(word)
    if len(list) == 0:
        print("No matches found")
    else:
        print(" ".join(list))


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    guesses_to_fail = 6
    flag = False
    letters_guessed = []
    warnings = 3
    hints_used = 0

    print('Welcome to the game, Hangman!')
    print('I am thinking of a word that is ' + str(len(secret_word)) +' letters long.')
    print('You have ' + str(warnings) +' warnings left.')
    print("-----------")

    while flag == False:
        print('You have ' + str(guesses_to_fail)  + ' guesses left.')
        print('Available letters: ' + get_available_letters(letters_guessed))
        guess = input('Please guess a letter: ').lower()

        if guess == "*":
            hints_used += 1
            print("Possible word matches are:")
            show_possible_matches(get_guessed_word(secret_word, letters_guessed))
            print("-----------")

        elif guess not in (get_available_letters(letters_guessed) and string.ascii_lowercase) and warnings > 0:
            warnings -= 1
            print("Oops! That is not a valid letter.", "You have " + str(warnings) + " warnings left:", get_guessed_word(secret_word, letters_guessed))
            print("-----------")

        elif guess not in (get_available_letters(letters_guessed) and string.ascii_lowercase) and warnings <= 0:
            warnings -= 1
            print("Oops! That is not a valid letter.", "You have no warnings left so you lose one guess:", get_guessed_word(secret_word, letters_guessed))
            print("-----------")
            guesses_to_fail -= 1

        elif guess not in get_available_letters(letters_guessed) and warnings > 0:
            warnings -= 1
            print("Oops! You've already guessed that letter.", "You have " + str(warnings) + " warnings left:", get_guessed_word(secret_word, letters_guessed))
            print("-----------")

        elif guess not in get_available_letters(letters_guessed) and warnings <= 0:
            warnings -= 1
            print("Oops! You've already guessed that letter.", "You have no warnings left so you lose one guess:", get_guessed_word(secret_word, letters_guessed))
            print("-----------")
            guesses_to_fail -= 1

        elif guess in secret_word and get_available_letters(letters_guessed):
            letters_guessed += [guess]
            print('Good guess: ' + get_guessed_word(secret_word, letters_guessed))
            print("-----------")

        elif guess not in secret_word and get_available_letters(letters_guessed):
            print('Oops! That letter is not in my word: ' + get_guessed_word(secret_word, letters_guessed))
            print("-----------")
            letters_guessed += [guess]
            if guess in 'aeiou':
              guesses_to_fail -= 2
            else:
              guesses_to_fail -= 1

        if is_word_guessed(secret_word, letters_guessed) == True:
            flag = True
            print("Congratulations, you won!")
            print("Your total score for this game is: " + str(guesses_to_fail * len(set(secret_word)) - hints_used))

        elif guesses_to_fail == 0:
            flag = True
            print('Sorry, you ran out of guesses. The word was ' + secret_word + '.')

# -----------------------------------

# Start the game
if __name__ == "__main__":
    #pass

    # To test the simple hangman, comment out the pass line above and
    # uncomment the following two lines.
    
    #secret_word = choose_word(wordlist)
    #hangman(secret_word)
    

    # To test a hangman with hints, re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)