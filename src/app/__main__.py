from chrome_trex import DinoGame, ACTION_UP, ACTION_FORWARD, ACTION_DOWN


FPS = 60

def initGame():

    game = DinoGame(FPS)

    action = ACTION_FORWARD

    score = 0

    dead_count = 0

    state = []

    while True:

        dino = game.player_dinos[0]
        state = game.get_state()
        score = game.get_score()

        game.step(action)

        if dino.is_dead:
            dead_count += 1
            if dead_count == 2:
                game.close()
                break
            
            game.reset()
    
    return score, state



def main():
    print("Joguinho funfando! YAY")
    score, state = initGame()
    print(f'Final score: {score}')
    print(f'States: {state}')



if __name__ == "__main__":
    SystemExit(main())
