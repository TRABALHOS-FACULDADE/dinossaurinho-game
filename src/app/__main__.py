import random as rnd
import numpy as np
from chrome_trex import DinoGame, ACTION_UP, ACTION_FORWARD, ACTION_DOWN

# Configurações do algoritmo genético
POPULATION_SIZE = 50
GENERATIONS = 100
MUTATION_RATE = 0.1
FPS = 60
BIAS = 0

game = DinoGame(FPS)

def softmax(x: list) -> np.ndarray:
    exp_x = np.exp(x)
    return exp_x / np.sum(exp_x)

class Dinossauro:
    def __init__(self) -> None:
        self.score = 0
        self.pesoForward = rnd.randint(0, 100) / 10
        self.pesoUp = rnd.randint(0, 100) / 10
        self.pesoDown = rnd.randint(0, 100) / 10
    

    def tomarDecisao(self, state: list) -> int:
        x_obs, y_obs = state[0], state[1]

        acao_up: float = x_obs * y_obs * self.pesoUp + BIAS
        acao_down: float = x_obs * y_obs * self.pesoDown + BIAS
        acao_forward: float = x_obs * y_obs * self.pesoForward + BIAS

        result = softmax([acao_forward, acao_up, acao_down]).tolist()
        
        return result.index(max(result))

def generate_dinos(population):
    return [Dinossauro() for _ in range(population)]

def run():

    dinos = generate_dinos(POPULATION_SIZE)

    i = 0

    while True:
        dino = game.player_dinos[0]
        player = dinos[i]
        acao = player.tomarDecisao(game.get_state())
        print(f'Geração 1 - Peso: F {player.pesoForward} U {player.pesoUp} D {player.pesoDown}')
        game.step(acao)
        if dino.is_dead:
            i += 1
            if i > POPULATION_SIZE:
                break
            game.reset()

if __name__ == '__main__':
    run()