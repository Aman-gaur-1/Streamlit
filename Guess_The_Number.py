import random
comp = random.randint(1,50)


chance = 1

while chance <= 10:
    user = int(input(f'Guess the number: '))

    if user == comp:
        print(f'You Won')
        print(f'Your Score : {110 - (chance*10)}')
        print()
        break

    elif user > comp:
        print(f'Hint: Guess Lower Number ')
        print(f'<---------- [Number of Chances Left : {10 - chance}] ---------->')


    elif user < comp:

        print(f'Hint: Guess Higher Number')
        print(f'<---------- [Number of Chances Left : {10 - chance}] ---------->')

    print()
    chance = chance + 1

else:
    print('You lose')
    print(f'Random Number: {comp}')

print('----------[Game over]----------')