import random as rnd
import numpy as np
from chrome_trex import MultiDinoGame, Dino, ACTION_UP, ACTION_FORWARD, ACTION_DOWN
import json

# Configurações do algoritmo genético
POPULATION_SIZE = 300
GENERATIONS = 200
MUTATION_RATE = 0.6
FPS = 400

game = MultiDinoGame(POPULATION_SIZE, FPS)

class Dinossauro:
    def __init__(self, gameDino: Dino) -> None:
        self.gameDino = gameDino
        self.pesos = [rnd.randint(-1000, 1000) for _ in range(10)]
    
    def tomarDecisao(self, state: list) -> int:
        avg = np.average(state, weights=self.pesos)
        
        return ACTION_UP if avg > 0 else ACTION_DOWN
    
    def mutate(self):
        for i in range(len(self.pesos)):
            prob = rnd.random()
            if prob <= MUTATION_RATE:
                self.pesos[i] = rnd.randint(-1000, 1000)

    def getPesos(self):
        return self.pesos

def dinoToJson(dino: Dinossauro, gen: int):
    with open('dinos.json', 'r') as file:
        lines = file.readlines()
        text = ''.join(lines)
        dinos: list = json.loads(text)
    
    dino_obj = {'geracao': gen, 'pesos_melhor_individuo': dino.getPesos()}
    dinos.append(dino_obj)

    with open('dinos.json', 'w') as file:
        file.write(json.dumps(dinos))


def selecao(dinos: list[Dinossauro]):
    return max(dinos, key=lambda d: d.gameDino.score)

def generate_dinos(population, gameDinos: list[Dino]):
    return [Dinossauro(gameDinos[i]) for i in range(population)]

def run():
    dinos = generate_dinos(POPULATION_SIZE, game.alive_players)
    dino_campeao = Dinossauro(Dino(44, 47))
    
    for gen in range(GENERATIONS):
    
        while len(game.alive_players) > 0:
            actions = [dino.tomarDecisao(state) for dino, state in zip(dinos, game.get_state())]
            game.step(actions)

        melhor_dino = selecao(dinos)
        dino_campeao = melhor_dino if melhor_dino.gameDino.score > dino_campeao.gameDino.score else dino_campeao

        # Repovoando jogo

        novos_dinos = [dino_campeao]

        for _ in range(POPULATION_SIZE-1):
            dino_campeao.mutate()
            novos_dinos.append(dino_campeao)


        game.reset()
        dinoToJson(dino_campeao, gen)

        for k in range(len(game.alive_players)):
            novos_dinos[k].gameDino = game.alive_players[k]


if __name__ == '__main__':
    run()
