from collections import deque
import random

class Ambiente:
    def __init__(self):
        self.estado = {'Q1': random.choice(['cheio', 'vazio']),
                       'Q2': random.choice(['cheio', 'vazio'])}
        self.accao = ['encher', 'esquerda', 'direita']

    def percepcao(self, agente):
        return (agente.localizacao, self.estado[agente.localizacao])

    def executar_accao(self, accao, agente):
        if accao == 'esquerda':
            agente.performance -= 1
            agente.localizacao = ('Q1' if agente.localizacao == 'Q2' else 'Q1')
        elif accao == 'direita':
            agente.performance -= 1
            agente.localizacao = ('Q2' if agente.localizacao == 'Q1' else 'Q2')
        elif accao == 'encher':
            agente.performance += 10
            self.estado[agente.localizacao] = "cheio"

class Agente:
    def __init__(self):
        self.performance = 0
        self.localizacao = 'Q1'
        self.modelo = {'Q1': None, 'Q2': None}
        self.direcao = 'direita'

    def programa(self, percepcao, ambiente):
        localizacao, estado = percepcao

        if estado == 'vazio':
            return 'encher'
        elif all(estado == 'cheio' for estado in self.modelo.values()):
            return 'parar'
        elif self.modelo[localizacao] == 'vazio':
            return 'encher'
        else:
            return self.bfs(ambiente, localizacao)

    def bfs(self, ambiente, start):
        fila = deque([(start, [])])  
        visitados = set()  

        while fila:
            posicao_atual, acoes = fila.popleft()  
            if ambiente.estado[posicao_atual] == 'vazio':
                return acoes[0]  

            if posicao_atual not in visitados:
                visitados.add(posicao_atual)
                for acao in ambiente.accao:
                    proxima_pos = self.obter_proxima_posicao(posicao_atual, acao)
                    if proxima_pos in ambiente.estado:
                        fila.append((proxima_pos, acoes + [acao]))

        return 'parar'

    def obter_proxima_posicao(self, posicao_atual, acao):
        if acao == 'esquerda':
            return 'Q1'
        elif acao == 'direita':
            return 'Q2'
        else:
            return posicao_atual

    def atualizar_modelo(self, percepcao, acao):
        localizacao, estado = percepcao
        if acao == 'encher':
            self.modelo[localizacao] = 'cheio'

# Main
ambiente = Ambiente()
agente = Agente()

print("Estado inicial do Ambiente:", ambiente.estado)

while True:
    todos_cheios = all(estado == 'cheio' for estado in ambiente.estado.values())
    if todos_cheios:
        print("Todos os baldes estão cheios. O agente parou.")
        break

    percepcao = ambiente.percepcao(agente)
    acao = agente.programa(percepcao, ambiente)

    ambiente.executar_accao(acao, agente)
    agente.atualizar_modelo(percepcao, acao)

    print("Percepção:", percepcao)
    print("Ação a Realizar:", acao)
    print("Pontuação:", agente.performance)
    print("Estado do Ambiente:", ambiente.estado)

print("Estado final do Ambiente:", ambiente.estado)
