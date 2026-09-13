import math

from world.game_state import GameState


def base_evaluation_function(state: GameState) -> float:
    """
    Retorna la evaluación base entregada para desarrollar el punto 4.

    Esta función no forma parte del código que debe modificar el estudiante y
    permite probar Minimax antes de desarrollar la heurística del punto 5.
    """
    if state.is_win():
        return 1000.0
    if state.is_lose():
        return -1000.0
    return float(state.get_score())


def evaluation_function(state: GameState) -> float:
    """
    Evalúa un estado desde la perspectiva del defensor MAX.

    Debe conservar las utilidades terminales de la evaluación base y diseñar
    una valoración no trivial para estados de corte. Minimax y alfa-beta usan
    esta misma función al comparar sus decisiones en el punto 5.

    Tips:
    - Los estados terminales ya se resuelven antes del bloque TODO; diseñe allí
      únicamente la valoración de estados no terminales.
    - Consulte state.defender_position, state.intruder_position,
      state.pending_terminals, state.get_score() y state.get_legal_actions(0).
    - state.layout.distance(start, goal) calcula y almacena en caché la distancia
      real por el mapa respetando los muros.
    - Maneje conjuntos vacíos y distancias infinitas, y mantenga todo estado no
      terminal estrictamente entre -1000 y +1000.
    """
    PESO_1 = 50.0
    PESO_2 = 50.0
    PESO_3 = 20.0
    PESO_4 = 10.0
    PESO_5 = 100.0
    DIVISOR_SCORE = 50.0
    if state.is_win() or state.is_lose():
        return base_evaluation_function(state)

    distancias = []
    for terminal in state.pending_terminals:
        distancias.append( state.layout.distance(state.defender_position, terminal) )
    distancia_terminal = min(distancias)
    cercania_terminal = 1 / (1 + distancia_terminal) 

    distancia_intruso = state.layout.distance(state.intruder_position, state.defender_position)
    cercania_intruso = 1 / (1 + distancia_intruso)    

    
    cantidad_pendientes = len(state.pending_terminals)

    movilidad = len(state.get_legal_actions(0))

    score = state.get_score()
    score_acotado = math.tanh(score / DIVISOR_SCORE)  
    valor = 0.0
    valor += PESO_1 * cercania_terminal        # más cerca de terminal = mejor -> suma
    valor -= PESO_2 * cercania_intruso         # más cerca del intruso = peor -> resta
    valor -= PESO_3 * cantidad_pendientes      # más pendientes = peor -> resta
    valor += PESO_4 * movilidad                # más movilidad = mejor -> suma
    valor += PESO_5 * score_acotado            # score alto = mejor -> suma

    return valor
