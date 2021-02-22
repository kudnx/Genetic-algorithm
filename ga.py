import random
import matriz

populacao = []  # lista que guarda os caminhos
tamanho_populacao = 10  # maximo de 120 combinações
probabilidade_mutacao = 0.1
numero_geracoes = 4
tamanho_rotas = [0] * tamanho_populacao
adaptacao = [0] * tamanho_populacao
melhor_caminho = 1000

cidades = matriz.cidades()

# matriz que contem as distâncias entre as cidades
distancias = matriz.matriz()


# calcula as distâncias entre duas cidades
def calcula_distancia(cidade1, cidade2):
    return distancias[cidade1][cidade2]


# cria uma rota randomica
def cria_rota():
    embaralhada = random.sample(cidades, len(cidades))
    return embaralhada


# calcula o tamanho de uma rota
def calcula_tam_rota():
    for i in range(tamanho_populacao):
        route1 = 0
        for j in range(1, len(cidades)):
            route1 = route1 + calcula_distancia(populacao[i][j - 1], populacao[i][j])
        tamanho_rotas[i] = route1
        adaptacao[i] = 1 / tamanho_rotas[i]


# cria a população inicial
def cria_populacao():
    for i in range(tamanho_populacao):
        populacao.append(cria_rota())


# trocaa probabilidade de 2 cidades em uma rota
def troca_mutacao(ind):
    selecionados = random.sample(range(len(cidades)), 2)
    temp = populacao[ind][selecionados[0]]
    populacao[ind][selecionados[0]] = populacao[ind][selecionados[1]]
    populacao[ind][selecionados[1]] = temp


# cruzamento parcial
def cruzamento_parcial(ind1, ind2):
    tamanho = len(cidades)
    p1, p2 = [0] * tamanho, [0] * tamanho

    # Inicializa a posição de cada indíce nos individuos
    for k in range(tamanho):
        p1[ind1[k]] = k
        p2[ind2[k]] = k
    # escolhe os pontos de cruzamento
    cxpoint1 = random.randint(0, tamanho)
    cxpoint2 = random.randint(0, tamanho - 1)
    if cxpoint2 >= cxpoint1:
        cxpoint2 += 1
    else:  # troca os dois pontos
        cxpoint1, cxpoint2 = cxpoint2, cxpoint1

    # Aplica o cruzamento entr os dois pontos
    for k in range(cxpoint1, cxpoint2):
        # mantem os valores selecionados guardados
        temp1 = ind1[k]
        temp2 = ind2[k]
        # troca os valores selecionados
        ind1[k], ind1[p1[temp2]] = temp2, temp1
        ind2[k], ind2[p2[temp1]] = temp1, temp2
        # marca a posição dos valores
        p1[temp1], p1[temp2] = p1[temp2], p1[temp1]
        p2[temp1], p2[temp2] = p2[temp2], p2[temp1]

    return ind1, ind2


# função que escolhe um pai de acordo com a adaptação seletiva
def selecao_roleta():
    s = 0
    parcial = 0
    ind = 0
    for m in range(tamanho_populacao):
        s = s + adaptacao[m]
    rand = random.uniform(0, s)
    for m in range(tamanho_populacao):
        if parcial < rand:
            parcial = parcial + adaptacao[m]
            ind = ind + 1
    if ind == tamanho_populacao:  # previne valores fora da lista
        ind = tamanho_populacao - 1
    return ind


# encontra o melhor caminho encontrado em cada geração
def acha_melhor():
    chave = 1000
    melhor = 0
    for i in range(tamanho_populacao):
        if tamanho_rotas[i] < chave:
            chave = tamanho_rotas[i]
            melhor = i
    return melhor


# inicializa algoritmo
cria_populacao()
print("Inicializa população:", "\n", populacao)
calcula_tam_rota()
print("Tamanho do caminho da população:", "\n", tamanho_rotas)

for j in range(numero_geracoes):
    for i in range(0, tamanho_populacao, 2):
        # escolhe os pais para o cruzamento
        pai1 = selecao_roleta()
        pai2 = selecao_roleta()
        # escolhe sempre os pais diferentes, não necessariamente
        while True:
            if pai1 == pai2:
                pai2 = selecao_roleta()
            else:
                break
        # atualiza a população
        populacao[i], populacao[i + 1] = cruzamento_parcial(populacao[pai1], populacao[pai2])
        # calcula o tamanho pra cada população gerada
        calcula_tam_rota()

    # escolhe os caminhos para a população de acordo com a probabilidade
    for i in range(tamanho_populacao):
        rand = random.uniform(0, 1)
        if rand < probabilidade_mutacao:
            troca_mutacao(i)

    # calcula o tamanho depois de cada mutação
    calcula_tam_rota()

    # acha o melhor caminho
    if tamanho_rotas[acha_melhor()] < melhor_caminho:
        index = acha_melhor()
        melhor_caminho = tamanho_rotas[index]

    print("Melhor caminho da geração", j + 1, ": ", populacao[acha_melhor()], "\n" "Tamanho do caminho: ",
          tamanho_rotas[acha_melhor()])
    print("População da geração", j + 1, ": \n", populacao)
    print("Tamanho dos caminhos:", tamanho_rotas, "\n")
print("O melhor caminho é:", populacao[index], "com o tamanho de", melhor_caminho)
