word = input("Type in the hangman word for your choice: ")

guesses = ''
turns = 10

while turns > 0:
    failed = 0

    for char in word:
        if char in guesses:
            print(char, end=' ')
        else:
            print('_', end=' ')
            failed += 1

    print()

    if failed == 0:
        print("You won")
        break

    guess = input("Guess a character: ")
    guesses += guess

    if guess not in word:
        turns -= 1
        print("Wrong")
        print("You have", turns, "more guesses")

        if turns == 0:
            print("You lose")
