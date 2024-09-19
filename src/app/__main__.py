import random as rnd
import numpy as np
from chrome_trex import MultiDinoGame, Dino, ACTION_UP, ACTION_FORWARD, ACTION_DOWN

# Configurações do algoritmo genético
POPULATION_SIZE = 50
GENERATIONS = 15
MUTATION_RATE = 0.3
FPS = 60
BIAS = 10

game = MultiDinoGame(POPULATION_SIZE, FPS)

class Dinossauro:
    def __init__(self, gameDino: Dino) -> None:
        self.gameDino = gameDino
        self.pesos = [rnd.randint(-1000, 1000) for _ in range(11)]
    
    def tomarDecisao(self, state: list) -> int:
        avg = np.average(state, weights=self.pesos)
        
        return ACTION_UP if avg > 0 else ACTION_DOWN
    
    def mutate(self):
        for i in range(len(self.pesos)):
            prob = rnd.random()
            if prob <= MUTATION_RATE:
                self.pesos[i] = rnd.randint(-1000, 1000)


def softmax(x: list) -> np.ndarray:
    exp_x = np.exp(x)
    return exp_x / np.sum(exp_x)

def selecao(dinos: list[Dinossauro]):
    return max(dinos, key=lambda d: d.gameDino.score)

def generate_dinos(population, gameDinos: list[Dino]):
    return [Dinossauro(gameDinos[i]) for i in range(population)]

def run():
    dinos = generate_dinos(POPULATION_SIZE, game.alive_players)
    
    for _ in range(GENERATIONS):
    
        while len(game.alive_players) > 0:
            actions = [dino.tomarDecisao(state) for dino, state in zip(dinos, game.get_state())]
            game.step(actions)

        melhor_dino = selecao(dinos)

        # Repovoando jogo

        novos_dinos = [melhor_dino]

        for _ in range(POPULATION_SIZE-1):
            melhor_dino.mutate()
            novos_dinos.append(melhor_dino)


        game.reset()

        for k in range(len(game.alive_players)):
            novos_dinos[k].gameDino = game.alive_players[k]


if __name__ == '__main__':
    run()
