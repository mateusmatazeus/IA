from collections import deque
import random

class Ambiente:
    def __init__(self):
        self.estado = {'Q1': random.choice(['cheio', 'vazio']),
                       'Q2': random.choice(['cheio', 'vazio'])}
        self.accao = ['encher', 'esquerda', 'direita']

    def percepcao(self, agente):
        return (agente.localizacao, self.estado[agente.localizacao])

    def localizacao_default(self):
        return random.choice(['Q1', 'Q2'])

    def executar_accao(self, accao, agente):
        if accao == 'esquerda':
            agente.performance -= 1
        elif accao == 'direita':
            agente.performance -= 1
        elif accao == 'encher':
            agente.performance += 10
            self.estado[agente.localizacao] = "cheio"

class Agente:
    def __init__(self, localizacao):
        self.performance = 0
        self.localizacao = localizacao

    def programa_tabela(self, percepcao):
        tabela = {('Q1', 'cheio'): 'direita',
                  ('Q1', 'vazio'): 'encher',
                  ('Q2', 'cheio'): 'esquerda',
                  ('Q2', 'vazio'): 'encher',
                  (('Q1', 'vazio'), ('Q1', 'cheio')): 'esquerda',
                  (('Q1', 'cheio'), ('Q2', 'vazio')): 'encher',
                  (('Q2', 'cheio'), ('Q1', 'vazio')): 'encher',
                  (('Q2', 'vazio'), ('Q2', 'cheio')): 'encher',
                  (('Q1', 'vazio'), ('Q1', 'cheio'), ('Q2', 'vazio')): 'encher',
                  (('Q2', 'vazio'), ('Q2', 'cheio'), ('Q1', 'vazio')): 'encher'}
        return tabela.get(percepcao)

def dfs(ambiente, initial_state):
    frontier = [initial_state]
    explored = set()

    while frontier:
        state = frontier.pop()

        if is_goal_state(state, ambiente):
            return state

        explored.add(state)

        for action in reversed(ambiente.accao):
            next_state = ambiente.resultado(state, action)
            if next_state not in explored and next_state not in frontier:
                frontier.append(next_state)

    return None

def is_goal_state(state, ambiente):
    return 'cheio' in state.values()

# Main
percepcoes = []
Q1, Q2 = 'Q1', 'Q2'

ambiente = Ambiente()
print("Estado do Ambiente:", ambiente.estado)
localizacao_agente = ambiente.localizacao_default()
agente = Agente(localizacao_agente)
percepcao = ambiente.percepcao(agente)
accao = agente.programa_tabela(percepcao)
ambiente.executar_accao(accao, agente)

print("Percepção:", percepcao)
print("Ação a Realizar:", accao)
print("Pontuação:", agente.performance)
print("Estado do Ambiente:", ambiente.estado)
print("Localização do Agente:", agente.localizacao)


localizacao_ant = agente.localizacao
localizacao_agente = Q1 if localizacao_ant == Q2 else Q2
agente.localizacao = localizacao_agente
percepcao = ambiente.percepcao(agente)
accao = agente.programa_tabela(percepcao)
ambiente.executar_accao(accao, agente)

print("\nDepois de mudar de localização:")
print("Percepção do novo Ambiente:", percepcao)
print("Ação a Realizar:", accao)
print("Pontuação:", agente.performance)
print("Estado do Ambiente:", ambiente.estado)
