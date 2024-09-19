import random

result = 0
playAgain = True

# Get player name
def get_player_name():
    user_name = input("Please enter your name: ")
    while len(user_name) > 10:
        print("Enter a name that is up to 10 characters.")
        user_name = input("Please enter your name: ")
    return user_name

user_name = get_player_name()
print(f"Welcome, {user_name}")

# Computer move
def computer_move():
    moves = ["rock", "paper", "scissors"]
    return random.choice(moves)

# Determine winner
def get_winner(player_move, computer_move):
    global result
    print(f"Player chose: {player_move}")
    print(f"Computer chose: {computer_move}")

    if (player_move == "rock" and computer_move == "paper") or \
       (player_move == "scissors" and computer_move == "rock") or \
       (player_move == "paper" and computer_move == "scissors"):
        result -= 1
        print(f"{result} - Computer wins")
    elif (player_move == "paper" and computer_move == "rock") or \
         (player_move == "scissors" and computer_move == "paper") or \
         (player_move == "rock" and computer_move == "scissors"):
        result += 1
        print(f"{result} - Player wins")
    else:
        print("Draw")

    return result

# Main game loop
while playAgain:
    player_move = input("Select either rock, paper, or scissors: ").lower()

    while player_move not in ["rock", "paper", "scissors"]:
        player_move = input("Select either rock, paper, or scissors: ").lower()

    computer_choice = computer_move()
    game_result = get_winner(player_move, computer_choice)
    print(f"Current score: {game_result}")

    playAgain = input("Do you want to play again? (yes/no): ").lower() == "yes"

print(f"Final score: {result}")
