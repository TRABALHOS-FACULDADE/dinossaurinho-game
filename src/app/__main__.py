import random as rnd
from chrome_trex import DinoGame, ACTION_UP, ACTION_FORWARD, ACTION_DOWN

# Função de aptidão
def fitness_function(game: DinoGame, individual):
    total_score = 0
    while not game.game_over:
        action = individual(game)
        game.step(action)
        total_score = game.get_score()
    return total_score

# Criação de um indivíduo aleatório
def create_individual():

    """
    Essa estratégia foi utilizada pois:
    
    ACTION_FORWARD = 0
    ACTION_UP = 1
    """

    return lambda _: ACTION_UP if rnd.random() < 0.5 else ACTION_FORWARD

# Cruzamento de indivíduos
def crossover(parent1, parent2):
    return lambda game: parent1(game) if rnd.random() < 0.5 else parent2(game)

# Mutação de um indivíduo
def mutate(individual, mutation_rate):
    def mutated_individual(game):
        action = individual(game)
        if rnd.random() < mutation_rate:
            if action == ACTION_UP:
                return ACTION_UP if rnd.random() < 0.5 else ACTION_FORWARD
            elif action == ACTION_FORWARD:
                return ACTION_FORWARD if rnd.random() < 0.5 else ACTION_UP
            else:
                return ACTION_UP if rnd.random() < 0.5 else ACTION_FORWARD
        return action
    return mutated_individual

# Algoritmo Genético
def genetic_algorithm(fps: int, generations, population_size, mutation_rate):
    population = [create_individual() for _ in range(population_size)]
    
    for generation in range(generations):
        scores = [fitness_function(DinoGame(fps), ind) for ind in population]
        
        # Seleção dos melhores indivíduos
        sorted_population = [x for _, x in sorted(zip(scores, population), key=lambda pair: pair[0], reverse=True)]
        best_individuals = sorted_population[:population_size // 2]
        
        # Cruzamento e mutação
        new_population = []
        while len(new_population) < population_size:
            parent1, parent2 = rnd.sample(best_individuals, 2)
            child = crossover(parent1, parent2)
            if rnd.random() < mutation_rate:
                child = mutate(child, mutation_rate)
            new_population.append(child)
        
        population = new_population
        
        # Exibindo dados do melhor indivíduo
        best_score = max(scores)
        print(f'Generation {generation + 1}, Best Score: {best_score}')
    
    return population[0], (generation+1), best_score

if __name__ == "__main__":

    FPS = 60
    generations = 10
    population_size = 10
    mutation_rate = 0.1

    best_individual, generation, score = genetic_algorithm(FPS, generations, population_size, mutation_rate)
    print(f'Best individual found!\nGeneration: {generation}\nScore: {score}')
