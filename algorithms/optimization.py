import math
import random

from optimization.problem import SmartGridOptimizationProblem
from optimization.result import Configuration, OptimizationResult


def configuration_score(
    problem: SmartGridOptimizationProblem, configuration: Configuration
) -> float:
    """
    Combina cobertura, redundancia y exposición en un puntaje a maximizar.

    Tips:
    - Use problem.score_components(configuration); ya retorna cobertura,
      redundancia y exposición en ese orden.
    """
    cobertura, redundancia, exposicion = problem.score_components(configuration)
    return cobertura-redundancia-exposicion 


def hill_climbing(
    problem: SmartGridOptimizationProblem,
    initial_configuration: Configuration,
    max_iterations: int = 500,
) -> OptimizationResult:
    """
    Ejecuta ascenso de colina con mejora estricta.

    Debe examinar todos los vecinos, seleccionar el de mayor puntaje y
    conservar el orden entregado por el problema para desempatar. La búsqueda
    termina cuando no existe una mejora estricta o se alcanza el límite.

    Tips:
    - problem.neighbors(current) retorna vecinos válidos en el orden que debe
      usarse para desempatar.
    - Cada llamada a configuration_score(...) cuenta como una evaluación.
    - Inicialice los historiales con la configuración inicial y agregue solo las
      mejoras aceptadas antes de retornar el OptimizationResult.
    """
    # TODO: Add your code here
    raise NotImplementedError("Punto 1: implemente hill_climbing")


def cooling_schedule(initial_temperature: float, cooling_rate: float, iteration: int) -> float:
    """
    Retorna el programa geométrico T(t) = T0 * alpha**t.

    Esta función se invoca desde simulated_annealing en cada iteración.
    """
    return initial_temperature * (cooling_rate**iteration)


def simulated_annealing(
    problem: SmartGridOptimizationProblem,
    initial_configuration: Configuration,
    initial_temperature: float = 20.0,
    cooling_rate: float = 0.97,
    max_iterations: int = 500,
    rng: random.Random | None = None,
) -> OptimizationResult:
    """
    Ejecuta recocido simulado para un problema de maximización.

    Debe proponer un vecino aleatorio por iteración, aceptar siempre las
    mejoras y aplicar exp(delta / temperature) en los demás casos. El estado
    actual y el mejor estado encontrado deben conservarse por separado.

    Tips:
    - Seleccione el candidato con rng.choice(problem.neighbors(current)) y use
      exclusivamente rng para conservar la reproducibilidad.
    - Obtenga la temperatura con cooling_schedule(...) y calcule la aceptación
      con delta = puntaje_candidato - puntaje_actual y math.exp(...).
    - Mantenga separados el estado actual y el mejor encontrado; registre el
      estado actual después de cada intento, incluso si se rechaza.
    - Detenga la ejecución cuando la temperatura alcance minimum_temperature.
    """
    rng = rng or random.Random()
    evaluations = 0
    minimum_temperature = 1e-9
    mejor = initial_configuration
    score_mejor = configuration_score(problem, mejor)
    evaluations += 1
    current = initial_configuration
    score_actual = configuration_score(problem, current)
    evaluations += 1
    history = []
    score_history =[]
    
    for i in range (max_iterations):
        temperatura = cooling_schedule(initial_temperature,cooling_rate,i)
        if temperatura < minimum_temperature:
            break

        vecinos = problem.neighbors(current) #vecinos de x estado 
        vecino = rng.choice(vecinos)
        score_vecino = configuration_score(problem, vecino)
        evaluations+= 1
        delta = score_vecino - score_actual
        if delta > 0: #si vecino es mejor a current actualizar current
            current = vecino
            score_actual = score_vecino
            if score_actual > score_mejor:  #si vecino es mejor que "mejor" actualiza mejor
                mejor = vecino
                score_mejor = configuration_score(problem, mejor) #cambia mejor y su score
                evaluations +=1
        else:
            probabilidad = math.exp(delta/temperatura)
            sorteo = rng.random()
            if probabilidad > sorteo: 
                current = vecino
                score_actual= score_vecino
                if score_actual > score_mejor:  #si vecino es mejor que "mejor" actualiza mejor
                    mejor = vecino
                    score_mejor = configuration_score(problem, mejor) #cambia mejor y su score
                    evaluations +=1
        history.append(current)
        score_history.append(score_actual)
    return OptimizationResult(
    best_configuration=mejor,
    best_score=score_mejor,
    evaluations=evaluations,
    iterations=i + 1,
    history=history,
    score_history=score_history,
)
                
                    
        
            
    


def one_point_crossover(
    parent1: Configuration, parent2: Configuration, rng: random.Random
) -> tuple[Configuration, Configuration]:
    """
    Realiza un cruce de un punto y retorna dos descendientes.

    La reparación de la cantidad de módulos se realiza posteriormente.

    Tips:
    - Seleccione con rng un corte interior, entre las posiciones 1 y len-1.
    - Cada descendiente combina el prefijo de un padre con el sufijo del otro.
    - Retorne tuplas y no repare aquí los descendientes.
    """
    if len(parent1) != len(parent2):
        raise ValueError("Los padres deben tener la misma longitud")
    if len(parent1) < 2:
        return parent1, parent2

    cut = rng.randint(1,len(parent1)-1)
    child1 = parent1[:cut] + parent2[cut:]
    child2 = parent2[:cut] + parent1[cut:]
    return child1, child2
  
    raise NotImplementedError("Punto 3: implemente one_point_crossover")


def swap_mutation(
    individual: Configuration, mutation_probability: float, rng: random.Random
) -> Configuration:
    """
    Aplica mutación por intercambio con la probabilidad indicada.

    Cuando ocurre una mutación, intercambia un bit activo y uno inactivo para
    conservar la cantidad de módulos instalados.

    Tips:
    - Use rng.random() para decidir si se aplica la mutación.
    - Identifique por separado los índices activos e inactivos y seleccione uno
      de cada grupo con rng.choice(...).
    - Si alguno de los dos grupos está vacío, no hay un intercambio posible.
    - Retorne una tupla nueva; no modifique el individuo recibido.
    """
    if rng.random() >= mutation_probability:
        return individual

    active = [index for index, bit in enumerate(individual) if bit]
    inactive = [index for index, bit in enumerate(individual) if not bit]
    if not active or not inactive:
        return individual

    on_index = rng.choice(active)
    off_index = rng.choice(inactive)

    mutated = list(individual)
    mutated[on_index] = 0
    mutated[off_index] = 1
    return tuple(mutated)
    raise NotImplementedError("Punto 3: implemente swap_mutation")


def genetic_algorithm(
    problem: SmartGridOptimizationProblem,
    population_size: int = 40,
    generations: int = 100,
    mutation_probability: float = 0.05,
    elite_size: int = 2,
    rng: random.Random | None = None,
) -> OptimizationResult:
    """
    Ejecuta un algoritmo genético generacional.

    Debe integrar la población inicial, la selección por torneo, el cruce, la
    reparación, la mutación y el elitismo entregados por el proyecto. Retorna
    el mejor individuo encontrado durante toda la ejecución.

    Tips:
    - Use problem.initial_population(...), problem.tournament_select(...) y
      problem.repair_configuration(...) para las operaciones ya entregadas.
    - Aplique one_point_crossover(...) antes de reparar y swap_mutation(...)
      después de la reparación.
    - Conserve los mejores individuos por elitismo y registre en los historiales
      el mejor global de cada generación.
    """
    rng = rng or random.Random()
    if population_size < 2:
        raise ValueError("La población debe tener al menos dos individuos")
    if generations < 0:
        raise ValueError("El número de generaciones no puede ser negativo")
    if not 0.0 <= mutation_probability <= 1.0:
        raise ValueError("La probabilidad de mutación debe estar entre 0 y 1")
    if not 0 <= elite_size <= population_size:
        raise ValueError("elite_size debe estar entre 0 y population_size")
    
    population = problem.initial_population(population_size, rng)
    scores = [configuration_score(problem, individual) for individual in population]
    evaluations = len(population)

    best_index = max(range(len(population)), key=lambda i: scores[i])
    best = population[best_index]
    best_score = scores[best_index]

    history = [best]
    score_history = [best_score]

    for _ in range(generations):
        ranked = sorted(range(len(population)), key=lambda i: scores[i], reverse=True)
        new_population = [population[i] for i in ranked[:elite_size]]

        while len(new_population) < population_size:
            parent1 = problem.tournament_select(population, scores, rng)
            parent2 = problem.tournament_select(population, scores, rng)
            child1, child2 = one_point_crossover(parent1, parent2, rng)

            child1 = problem.repair_configuration(child1, rng)
            child1 = swap_mutation(child1, mutation_probability, rng)
            new_population.append(child1)

            if len(new_population) < population_size:
                child2 = problem.repair_configuration(child2, rng)
                child2 = swap_mutation(child2, mutation_probability, rng)
                new_population.append(child2)

        population = new_population
        scores = [configuration_score(problem, individual) for individual in population]
        evaluations += len(population)

        generation_best_index = max(range(len(population)), key=lambda i: scores[i])
        if scores[generation_best_index] > best_score:
            best = population[generation_best_index]
            best_score = scores[generation_best_index]

        history.append(best)
        score_history.append(best_score)

    return OptimizationResult(
        best_configuration=best,
        best_score=best_score,
        evaluations=evaluations,
        iterations=generations,
        history=history,
        score_history=score_history,
    )
    raise NotImplementedError("Punto 3: implemente genetic_algorithm")
