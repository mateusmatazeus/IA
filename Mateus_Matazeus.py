import random

class Ambiente:
    def _init_(self):
        self.estado = {(0,0): random.choice(['cheio', 'vazio']),
                       (1,0): random.choice(['cheio', 'vazio']),
                       (2,0): random.choice(['cheio', 'vazio'])}
        self.accao = ['encher', 'esquerda', 'direita']

    def percepcao(self, agente):
        return (agente.localizacao, self.estado[agente.localizacao])

    def executar_accao(self, accao, agente):
        if accao == 'esquerda':
            agente.performance -= 1
            agente.localizacao = (agente.localizacao[0] - 1, agente.localizacao[1])
        elif accao == 'direita':
            agente.performance -= 1
            agente.localizacao = (agente.localizacao[0] + 1, agente.localizacao[1])
        elif accao == 'encher':
            agente.performance += 10
            self.estado[agente.localizacao] = "cheio"

class Agente:
    def _init_(self):
        self.performance = 0
        self.localizacao = (0, 0)
        self.modelo = {posicao: None for posicao in [(0,0), (1,0), (2,0)]}
        self.direcao = 'direita'

    def programa(self, percepcao):
        localizacao, estado = percepcao

        if estado == 'vazio':
            return 'encher'
        elif all(estado == 'cheio' for estado in self.modelo.values()):
            return 'parar'
        elif self.modelo[localizacao] == 'vazio':
            return 'encher'
        elif localizacao[0] < 2:
            return 'direita'
        else:
            return 'esquerda'

    def atualizar_modelo(self, percepcao, accao):
        localizacao, estado = percepcao
        if accao == 'encher':
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
    accao = agente.programa(percepcao)

    ambiente.executar_accao(accao, agente)
    agente.atualizar_modelo(percepcao, accao)

    print("\nO agente se moveu e interagiu com o ambiente.")
    print("Percepção:", percepcao)
    print("Ação a Realizar:", accao)
    print("Pontuação:", agente.performance)
    print("Estado do Ambiente:", ambiente.estado)

print("Estado final do Ambiente:", ambiente.estado)