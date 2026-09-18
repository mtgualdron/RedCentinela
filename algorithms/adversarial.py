from abc import ABC, abstractmethod

from algorithms.evaluation import evaluation_function
from world.game_state import GameState
import math


class MultiAgentSearchAgent(ABC):
    """Clase base para los agentes de búsqueda adversaria."""

    def __init__(self, depth: int | str = 2) -> None:
        self.depth = int(depth)
        if self.depth < 1:
            raise ValueError("La profundidad debe ser al menos 1 ply")
        self.nodes_evaluated = 0

    @abstractmethod
    def get_action(self, state: GameState) -> str | None:
        raise NotImplementedError


class MinimaxAgent(MultiAgentSearchAgent):
    """Agente Minimax para el defensor MAX frente al intruso MIN."""

    def get_action(self, state: GameState) -> str | None:
        """
        Retorna la acción del defensor con mayor valor Minimax.

        El defensor es MAX (agente 0), el intruso es MIN (agente 1) y cada
        acción consume un ply. Debe respetar el orden de las acciones legales,
        usar evaluation_function en terminales y cortes, y contar cada estado
        procesado una vez en self.nodes_evaluated, incluida la raíz.

        Tips:
        - Use state.get_legal_actions(agent_index) y
          state.generate_successor(agent_index, action) para expandir el árbol.
        - Compruebe state.is_win(), state.is_lose() y el corte de profundidad;
          evalúe esos estados con evaluation_function(state).
        - El siguiente agente es (agent_index + 1) % state.get_num_agents().
          depth=1 incluye una acción de MAX y depth=2 una de MAX y una de MIN.
        - Reinicie las métricas y cuente una vez cada estado procesado, incluida
          la raíz. Retorne la acción de MAX y conserve la primera en los empates.
        """
        # TODO: Add your code here
        self.nodes_evaluated = 0
        self.nodes_evaluated+=1
        mejor_valor = -999999999999999999999999999999999
        mejor_accion = None
        acciones = state.get_legal_actions(0)
        for accion in acciones:
          sucesor = state.generate_successor(0, accion)
          v = self.valor(sucesor, 1, 1)
          if v > mejor_valor:
            mejor_valor = v
            mejor_accion = accion
        return mejor_accion
        
    def valor(self, state: GameState, agente, profundidad): #funcion aux recursiva que simula las rutas de los sucesores ;)
      self.nodes_evaluated+=1
      if state.is_win() or state.is_lose() or profundidad == self.depth:
        return evaluation_function(state)
      else:
        acciones = state.get_legal_actions(agente)
        if agente == 0:
          mejor_valor = -99999999999999999999999999999999
          for accion in acciones:
            sucesor = state.generate_successor(agente, accion)
            siguiente = (agente+1)%state.get_num_agents()
            valor_generado = self.valor(sucesor, siguiente, profundidad+1)
            mejor_valor = max(mejor_valor, valor_generado)
          return mejor_valor
        elif agente == 1:
          menor_valor = 99999999999999999999999999999999
          for accion in acciones:
            sucesor = state.generate_successor(agente, accion)
            siguiente = (agente+1)%state.get_num_agents()
            valor_generado = self.valor(sucesor, siguiente, profundidad+1)
            menor_valor = min(menor_valor, valor_generado)
          return menor_valor
        
      
      


class AlphaBetaAgent(MultiAgentSearchAgent):
    """Agente Minimax que evita explorar ramas mediante poda alfa-beta."""

    def get_action(self, state: GameState) -> str | None:
        """
        Retorna la acción de Minimax aplicando poda alfa-beta.

        Debe usar la misma profundidad, orden de acciones y función de
        evaluación que Minimax.

        Tips:
        - Conserve la misma estructura y casos base de MinimaxAgent.
        - Inicie alpha en -infinito y beta en +infinito, y páselos en las
          llamadas recursivas.
        - En MAX actualice alpha y corte si valor >= beta; en MIN actualice beta
          y corte si valor <= alpha.
        """
        self.nodes_evaluated = 0
        self.nodes_evaluated +=1
        alpha = -math.inf
        beta = math.inf
        mejor_valor = -math.inf
        mejor_accion = None

        for accion in state.get_legal_actions(0):
          sucesor = state.generate_successor(0, accion)
          valor = self._valor(sucesor, 1, 1, alpha, beta)
          if valor > mejor_valor:
              mejor_valor = valor
              mejor_accion = accion
              alpha = max(alpha, mejor_valor)
              

        return mejor_accion
    
    def _valor(self,state:GameState,agente,profundidad,alpha,beta):
      self.nodes_evaluated+=1
      if state.is_win() or state.is_lose():
        return evaluation_function(state)
      if profundidad == self.depth:
        return evaluation_function(state)
      acciones = state.get_legal_actions(agente)
      siguiente = (agente + 1) % state.get_num_agents()
      if agente == 0:   # MAX
        mejor_valor = -math.inf
        for accion in acciones:
            sucesor = state.generate_successor(agente, accion)
            v = self._valor(sucesor, siguiente, profundidad + 1, alpha, beta)
            mejor_valor = max(mejor_valor, v)
            alpha = max(alpha, mejor_valor)
            if mejor_valor >= beta:
                break
        return mejor_valor
      else: 
        mejor_valor = math.inf
        for accion in acciones:
            sucesor = state.generate_successor(agente, accion)
            v = self._valor(sucesor, siguiente, profundidad + 1, alpha, beta)
            mejor_valor = min(mejor_valor, v)
            beta = min(beta, mejor_valor)
            if mejor_valor <= alpha:
                break
        return mejor_valor
        
      
