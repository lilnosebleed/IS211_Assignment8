import argparse
import random
import time

## game objects
class Die:
    ## handles the random rolling logic
    def roll(self):
        return random.randint(1, 6)

class Player:
    """
    Base class (Parent). 
    Sets up the standard attributes every player needs.
    """
    def __init__(self, name):
        self.name = name
        self.score = 0

    def take_turn(self):
        ## blueprint for now
        ## the child classes below will override this with actual rules.
        
        pass 

class HumanPlayer(Player):
  ## child class inherits from Player and also handles user input
    def take_turn(self):
        turn_total = 0
        die = Die()
        
        while True:
            print(f"\n{self.name}'s Turn. Current Score: {self.score} | Turn Total: {turn_total}")
            choice = input("Roll (r) or Hold (h)? ").lower()
            
            if choice == 'r':
                roll_val = die.roll()
                print(f"Rolled a {roll_val}")
                if roll_val == 1:
                    print("Pig! You lose your points for this turn.")
                    turn_total = 0
                    break
                else:
                    turn_total += roll_val
            elif choice == 'h':
                break
            else:
                print("Invalid input.")
                
        self.score += turn_total
        print(f"{self.name}'s total score is now {self.score}")

class ComputerPlayer(Player):
    ## child classes inherits from player and also handles the automated ai
    def take_turn(self):
        turn_total = 0
        die = Die()
        
        ## the specific AI strategy requested by the assignment rules.
        ## it calculates how far the computer is from 100, and stops at either 25 or that difference.
        limit = min(25, 100 - self.score)
        print(f"\n{self.name}'s Turn (Computer). Target is {limit}.")
        
        while turn_total < limit:
            roll_val = die.roll()
            print(f"Computer rolled a {roll_val}")
            
            if roll_val == 1:
                print("Pig! Computer loses its points for this turn.")
                turn_total = 0
                break
            else:
                turn_total += roll_val
                
        self.score += turn_total
        print(f"{self.name} holds. Total score is now {self.score}")



## using factory design pattern
class PlayerFactory:
    ## the factory pattern handles object creation.
    ## instead of cluttering our main code with if/else statements to figure out which class to use, we just tell the factory make a human or make a computer

    
    def get_player(self, player_type, name):
        if player_type.lower() == "human":
            return HumanPlayer(name)
        elif player_type.lower() == "computer":
            return ComputerPlayer(name)


## using proxy design pattern, acting as the game engine

class Game:
    ## the standard version of the game which is also untimed
    def __init__(self, player1, player2):
        self.players = [player1, player2]

    def play(self):
        random.seed(0)
        current = 0
        
        ## keep playing as long as both players are under 100 points
        while self.players[0].score < 100 and self.players[1].score < 100:
            self.players[current].take_turn()
            
            if self.players[current].score >= 100:
                print(f"\n{self.players[current].name} wins the game!")
                return
                
            ## swap between player 0 and player 1
            current = 1 - current 

class TimedGameProxy
    ## the proxy pattern acts as a wrapper around the original Game class.
    ## it allows us to add the 60-second timer feature without having to modify or break the original Game class code above.
    
    def __init__(self, player1, player2):
        ## the proxy creates and holds the real game object inside itself
        self.game = Game(player1, player2)

    def play(self):
        random.seed(0)
        start_time = time.time()
        current = 0
        
        while self.game.players[0].score < 100 and self.game.players[1].score < 100:
            
            ## checks the timer before a turn has begun
            if time.time() - start_time >= 60:
                print("\nTime is up! 60 seconds have passed.")
                break
                
            ## executes the turn using the original game's players
            self.game.players[current].take_turn()
            
            ## checks timer again after the game.round is over
            if time.time() - start_time >= 60:
                print("\nTime is up! 60 seconds have passed.")
                break

            ## checks win condition 
            if self.game.players[current].score >= 100:
                print(f"\n{self.game.players[current].name} wins the game!")
                return
                
            current = 1 - current
            
        ## tallies the points to find winner if timer breaks the loop
        p1 = self.game.players[0]
        p2 = self.game.players[1]
        print(f"\nFinal Score - {p1.name}: {p1.score}, {p2.name}: {p2.score}")
        if p1.score > p2.score:
            print(f"{p1.name} wins on time!")
        elif p2.score > p1.score:
            print(f"{p2.name} wins on time!")
        else:
            print("It's a tie!")


##  output
if __name__ == "__main__":
    # setup argparse to accept command line inputs
    parser = argparse.ArgumentParser()
    parser.add_argument('--player1', type=str, default='human')
    parser.add_argument('--player2', type=str, default='computer')
    parser.add_argument('--timed', action='store_true')
  
    args, unkown = parser.parse_known_args()

    ## use the Factory to create our players based on the arguments
    factory = PlayerFactory()
    p1 = factory.get_player(args.player1, "Player 1")
    p2 = factory.get_player(args.player2, "Player 2")

    ## if timed was used, run the Proxy. Otherwise, run the standard Game.
    if args.timed:
        proxy = TimedGameProxy(p1, p2)
        proxy.play()
    else:
        game = Game(p1, p2)
        game.play()
