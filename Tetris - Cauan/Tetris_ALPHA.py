# Autor: Cauan Dos Reis Almeida
# Componente Curricular: MI Algoritmos
# Concluído em: 27 de outubro de 2024
# Declaro que este código foi elaborado por mim de forma individual e não contém nenhum
# trecho de código de outro colega ou de outro autor, tais como provindos de livros e
# apostilas, e páginas ou documentos eletrônicos da Internet. Qualquer trecho de código
# de outra autoria que não a minha está destacado com uma citação para o autor e a fonte
# do código, e estou ciente que estes trechos não serão considerados para fins de avaliação.


#imports e inits necessários para o funcionamento do código.
import random
import os
import time
import pygame #Pip necessário.
import numpy as np #Pip necessário.
import pyfiglet #pip necessário.
#Funções do pygame necessária para a leitura do teclado e acréscimo de musica.
pygame.init()
screen = pygame.display.set_mode((1,1))
pygame.display.set_caption('1')

#Conjunto de cores para deixar as peças e a interface com visibilidade facilitada e mais bela.
Vermelho = '\033[0;31m'
Rosa_claro = '\033[38;5;205m'
Roxo = '\033[38;5;93m'
Azul = '\033[0;34m'
Laranja = '\033[38;5;208m'
Amarelo = '\033[0;33m'
Marrom_escuro = '\033[38;5;94m'
#Conjunto de cores para deixar a interface com visibilidade facilitada e mais bela.
Magenta = '\033[0;35m'
Ciano = '\033[0;36m'
Amarelo_claro = '\033[38;5;229m'
Fundo_roxo = '\033[1m\033[48;5;93m'
#Reset das cores.
Reset = '\033[0m'

#Peças do jogo.
peça_L = [['1', 0], ['1', 0], ['1', '1']]
peça_T = [['1', '1', '1'], [0, '1', 0]]
peça_J = [[0, '1'], [0, '1'], ['1', '1']]
peça_S = [[0, '1', '1'], ['1', '1', 0]]
peça_Z = [['1', '1', 0], [0, '1', '1']]
peça_I = [['1', '1', '1', '1']]
peça_I_5_blocos = [['1','1','1','1','1']]
peça_O = [['1', '1'], ['1', '1']]
peça_O_3x3 = [['1','1','1'],['1','1','1'],['1','1','1']]
Bomba_3x3 = [['💣']]

#Puxa a pasta e as músicas nela pra tocar durante o jogo.
Trilha_folder = 'Tetris - Cauan'
Trilha_sonora = [musica for musica in os.listdir(Trilha_folder) if musica.endswith('.mp3')]

#Tabuleiro apenas com '0' e '!', ou seja, vazio e com bordas laterais.
tabuleiro = [['!','0','0','0','0','0','0','0','0','0','0','!'] for i in range(20)]
#Criação e adiconamento de bordas superior e inferior pra limitação e embelezamento do tabuleiro.
tab2 = ['!','9','9','9','9','9','9','9','9','9','9','!']
tabuleiro.insert(0, tab2)
tabuleiro.append(tab2)

#Finção que limpa o terminal.
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

#Escolhe uma música pra tocar.
def toca_musica_aleatoria():
    seleciona_musica = random.choice(Trilha_sonora)
    pygame.mixer.music.load(os.path.join(Trilha_folder,seleciona_musica))
    pygame.mixer.music.play(-1)

#Separador de mensagens no terminal
def separador():
    sep = 33*f'{Magenta}={Reset}{Roxo}-{Reset}{Ciano}={Reset}'
    return sep

#Função que sorteia qual peça entrará no tabuleiro.
def sorteio():
    peças = [peça_L, peça_T, peça_S, peça_Z, peça_I, peça_O, peça_O_3x3, peça_I_5_blocos, Bomba_3x3]
    #Escolhe um valor entre 0 e 3 para determinar rotação da peça.
    rot = random.randint(0,4)
    #Rotaciona a peça.
    escolha_rotacionada = np.rot90(random.choice(peças),k=rot) 
    #Retorna a peça com a devida rotação.
    return escolha_rotacionada

#Imprime o tabuleiro no terminal com todas as atualizações durante o jogo.
def Game(pont):
    #Limpa o terminal antes de mostrar o tabbuleiro atualizado.
    clear()
    loc_x = 0
    for  linha in tabuleiro:
        print(" "*100 ,end='')
        for elemento in linha:
            print(elemento, end='  ')
            #variável usada para imprimir a pontuação na primmeira linha ao lado do tabuleiro.
            if loc_x == 11:
                print(f"""SCORE: {pont:09}""", end='')
            loc_x += 1
        print()

#Função que lê o teclado quando um tecla é pressionada.
def direcional():
    pygame.event.pump()
    direção = ''
    #Lê se a tecla está sendo pressionada e retorna uma direção correspondente à tecla.
    tecla = pygame.key.get_pressed()
    if tecla[pygame.K_RIGHT]:
        direção = 'direita'
    if tecla[pygame.K_LEFT]:
        direção = 'esquerda'
    if tecla[pygame.K_DOWN]:
        direção = 'baixo'
    #Para a tecla UP foi usado um formato diferente para evitar giro infinito.
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                direção = 'cima'
    return direção

#Lê qual a peça que foi sorteada e retorna sua cor.
def cores(peça):
    cor = ''
    #Uso de for comprimido para facilitar e diminuir o código. Lê todas as rotações da peça.
    if any(np.array_equal(peça,np.rot90(peça_L,k)) for k in range(4)):
        cor = Rosa_claro
    elif any(np.array_equal(peça,np.rot90(peça_T,k)) for k in range(4)):
        cor = Roxo
    elif any(np.array_equal(peça,np.rot90(peça_J,k)) for k in range(4)):
        cor = Azul
    #Uso de for comprimido de forma diferente devido as peças S e Z ter apenas uma rotação.
    elif any(np.array_equal(peça,s_peça) for s_peça in [peça_S,np.rot90(peça_S)]):
        cor = Amarelo
    elif any(np.array_equal(peça,z_peça) for z_peça in [peça_Z,np.rot90(peça_Z)]):
        cor = Marrom_escuro
    #Uso de for de forma diferente devido o fato de ter mais de uma peça com a mesma cor e só ter uma rotação.
    elif any(np.array_equal(peça,i_peça) for i_peça in [peça_I,np.rot90(peça_I),peça_I_5_blocos,np.rot90(peça_I_5_blocos)]):
        cor = Laranja
    elif any(np.array_equal(peça,o_peça) for o_peça in [peça_O,peça_O_3x3]):
        cor = Vermelho
    return cor

#Função que atualiza as posições das peças sempre que necessário.
def atualizar_tabuleiro(peça,y,x,valor):
    cor = cores(peça)
    for i in range(len(peça)):
        for j in range(len(peça[0])):
            if peça[i][j] == '1':
                if valor != '0':
                    valor = f'{cor}1{Reset}'
                tabuleiro[y+i][x+j] = valor
            elif peça[i][j] == '💣':
                if valor != '0':
                    valor = '💣'
                tabuleiro[y+i][x+j] = valor

#Função que faz a remoção de peças '1' quando em contato com a bomba.
def explosão(peça,y,x,pont):
    if np.array_equal(peça,Bomba_3x3):
        for i in range(-1,2):
            for j in range(-1,2):
                if tabuleiro[y+(i)][x+(j)] != '!' and tabuleiro[y+(i)][x+(j)] != '0' and tabuleiro[y+(i)][x+(j)] != '9':
                    tabuleiro[y+(i)][x+(j)] = '0'
                    Game(pont)
                time.sleep(0.5)

#Função que aumenta a pontuação.
def score(valor_pont,lin):
    if lin == 1:
        valor_pont += 10
    elif lin == 2:
        valor_pont += (10*2)
    elif lin == 3:
        valor_pont += (10*5)
    elif lin == 4:
        valor_pont += (10*10)
    elif lin == 5:
        valor_pont += (10*25)
    return valor_pont

#Função que lê o tabuleiro e determina se a peça pode ou não cair. 
def leitura_queda(peça,y,x):
    cor = cores(peça)
    numero_de_zero = 0
    for i in range(len(peça)):
        for j in range(len(peça[0])):
            if tabuleiro[y+i][x+j] == f'{cor}1{Reset}' or tabuleiro[y+i][x+j] == '💣':
                if tabuleiro[y+i+1][x+j] == '0':
                    numero_de_zero += 1
    return numero_de_zero

#Função que lê se a peça pode ou não ir pra direita/esquerda.
def move_x(peça,y,x):
    cor = cores(peça)
    x_direita = 0
    x_esquerda = 0
    for i in range(len(peça)):
        for j in range(len(peça[0])):
            if tabuleiro[y+i][x+j] == f'{cor}1{Reset}':
                if tabuleiro[y+i][x+j+1] == '0':
                    x_direita += 1
                if tabuleiro[y+i][x+j-1] == '0':
                    x_esquerda += 1
    return x_direita,x_esquerda

#Função que lê a dificuldade e retorna um tempo.
def tempo_de_queda(diff):
    if diff == '1':
        tempo = 0.9
    elif diff == '2':
        tempo = 0.5
    elif diff == '3':
        tempo = 0.2
    elif diff == '4':
        tempo = 0.05
    elif diff == '5':
        tempo = 0.01
    return tempo

#Verifica se todas as posições necessárias pra peça rotacionada estão livres.
def giro(peça,y,x):
    num_0 = []
    peça_rot = np.rot90(peça,k=1)
    for i in range(len(peça_rot)):
        for j in range(len(peça_rot[0])):
            if peça_rot[i][j] != '0':
                if  0 <= y+i < len(tabuleiro) and 0 <= x+j < len(tabuleiro[0]) and tabuleiro[y+i][x+j] == '0':
                    num_0.append(True)
                else:
                    num_0.append(False)
    return all(num_0)

#Função que limpa o tabuleiro após um jogo.
def limpa_tabulas(y,x):
    for i in range(1,21):
        for j in range(1,11):
            tabuleiro[y+i][x+j] = '0'

#Função principal onde o jogo ocorre.
def Inicializa_jogo(peça,pont,diff,primeira_musica_tocada):
    #Variáveis que determinam onde a peça será impressa.
    linha = 1
    coluna = random.randint(1, 11-len(peça[0]))

    #Imprime a peça na posição inical.
    atualizar_tabuleiro(peça,linha,coluna,1)
    Game(pont)

    #Variável que inicializa o while que faz a peça se mover.
    fim = 0
    #Variáveis para calcular ultimo tempo que a peça caiu.
    intervalo_queda = tempo_de_queda(diff)
    ultimo_tempo = time.time()
    #While  que faz a peça continuar se movendo até colidir.
    while fim == 0:
        #Variáveis de tempo.
        tempo_atual = time.time()
        tempo_passado = tempo_atual - ultimo_tempo

        #Variável que guarda o valor da tecla pressionada.
        direção = direcional()
        
        #Variável que guarda os valores para movimentação direita/esquerda.
        pode_direita, pode_esquerda= move_x(peça,linha,coluna)

        #Atualiza a peça pra direita quando clica/pressiona pra direita.
        if direção == 'direita' and pode_direita == len(peça):
            atualizar_tabuleiro(peça,linha,coluna,'0')
            coluna += 1
            atualizar_tabuleiro(peça,linha,coluna,1)

        #Atualiza a peça pra esquerda quando clica/pressiona pra esquerda.
        if direção == 'esquerda' and pode_esquerda == len(peça):
            atualizar_tabuleiro(peça,linha,coluna,'0')
            coluna -= 1
            atualizar_tabuleiro(peça,linha,coluna,1)

        #Rotaciona a peça quando clica para cima.
        if direção == 'cima':
            atualizar_tabuleiro(peça,linha,coluna,'0')
            coluna_tira_len_menos2 = []
            if tabuleiro[linha][coluna+len(peça[0])] == '!':
                #Verifica se a peça está no canto do tabuleiro e retira posições para ela girar.
                #Não funciona pra Peça_I e peça_I_5_blocos na vertical.
                coluna -= len(peça) - 2
            #Verifica se pode ser girada.
            pode_girar = giro(peça,linha,coluna)
            if not pode_girar == False:
                peça = np.rot90(peça,k=1)
            atualizar_tabuleiro(peça,linha,coluna,1)

        #Aumenta a velocidade que a peça cai quando clica/pressiona para baixo.
        if direção == 'baixo':
            ultimo_tempo = intervalo_queda - 0.5

        #verifica se o tempo desde que a ultima queda é igual ao intervalo definido pra queda.
        if tempo_passado >= intervalo_queda:
            pode_cair = leitura_queda(peça,linha,coluna)
            #Verifica se pode cair.
            if pode_cair == len(peça[0]):
                atualizar_tabuleiro(peça,linha,coluna,'0')
                linha += 1
                atualizar_tabuleiro(peça,linha,coluna,1)
                #Atualiza o tempo.
                ultimo_tempo = tempo_atual

            #Finaliza o while quando a peça não pode mais cair.
            else: 
                fim = 1
        #Atraso do tempo para não sobrecarregar o while.
        time.sleep(0.03)

        #Imprime o tabuleiro e a pontuação atualizados.
        Game(pont)
        #Verifica se há uma música tocando e toca caso não haja.
        if not pygame.mixer.music.get_busy() and not primeira_musica_tocada:
            primeira_musica_tocada = True
            toca_musica_aleatoria()
        #Chama e executa  a função de explosão da bomba após imprimir sua ultima posição no tabuleiro.
        if tabuleiro[linha+1][coluna] != '0':
            explosão(peça,linha,coluna,pont)

#programa principal.
#Limpa o terminal e mostra uma mensagem de boas vindas e um menu.
clear()
print(separador() + Fundo_roxo + f'\n{"THE BINARY TETRIS":^100}\n' + f'{"JUNGUICUQUI APPS":^100}\n' + Reset + separador())
time.sleep(2)
print(Amarelo_claro + f'{"Seja bem vindo ao meu tetris!":^100}\n' + f'{"Espero que goste da jogatina.":^100}\n' f'{"DEV:CAUAN DOS REIS ALMEIDA":^100}\n' + Reset)
time.sleep(1.5)

#variável que determina a dificuldade do jogo.
dificuldade = '1'
#Fonte para mensagem de game over.
texto_derrota = pyfiglet.Figlet(font='big')
#Variável que mantém o programa rodando.
interface = 'Abrir'
#While que é todo o programa.
while interface != 'Fechar':
    #Música de inicio desse tetris, toda vez que recomeçar vai tocar ela.
    primeira_musica = 'STRAY KIDS - 락 (樂) (LALALALA) 【8bit ⧸ Videogame ver.】_[cut_169sec].mp3'
    #Função que pegar a musica na pasta.
    primeiro_path = os.path.join(Trilha_folder,primeira_musica)
    print(separador())
    #Tela menu do jogo.
    função = input(f'{"[1] Jogar":^100}\n'
                f'{"[2] Dificuldade":^100}\n'
                f'{"[3] Fechar programa":^100}\n')

    if função not in ['1','2','3']:
        while função not in ['1','2','3']:
            clear()
            print(f'{"DIGITE 1,2 OU 3":^100}')
            função = input(f'{"[1] Jogar":^100}\n'
                        f'{"[2] Dificuldade":^100}\n'
                        f'{"[3] Fechar programa":^100}\n')
    #Inicia o jogo.
    elif função == "1":
        #toca a primeira musica.
        pygame.mixer.music.load(primeiro_path)
        pygame.mixer.music.play()
        #Variavel que ve se a primeira musica ja foi tocada.
        primeira_musica_tocada = False
        #Mensagens para preparar o jogador pro jogo no ritmo da musica.
        print(separador())
        print(f'{"PREPARADO?":^100}\n')
        time.sleep(3)
        print(f'{"3":^100}\n')
        time.sleep(1)
        print(f'{"2":^100}\n')
        time.sleep(1)
        print(f'{"1":^100}\n')
        time.sleep(1)
        print(f'{"JÁ":^100}')
        time.sleep(1)
        #A cor é definida com '' no início pois um obejto pintado recebe junto o código da cor, oq dificulta a leitura do python.
        cor = ''
        pontuação = 0
        #Verifica se já ocorreu um jogo.
        if any(tabuleiro[1][x] != '0' for x in range(1,11)):
            y = 0
            x = 0
            limpa_tabulas(y,x)
        #While quem mantém o jogo 'rodando' enquanto a primeira linha vazia do tabuleiro não possuir uma peça.
        while f'{cor}1{Reset}' not in tabuleiro[1]:
            #Chama a função que escolhe a peça e guarda seu valor para após verificar a condição do while.
            peça = sorteio()
            Inicializa_jogo(peça,pontuação,dificuldade,primeira_musica_tocada) #Inicializa o jogo.
            cor = cores(peça) #Guarda o valor da cor para verificação do while.
            n_linhas = 0 #Variável para limpeza das linhas.
            for i in range(1,21): #Passa linha por linha do tabuleiro de '0'.
                if all(line.strip() != '0' for line in tabuleiro[i]): #Verifica se toda a linha é diferente de '0'.
                    n_linhas += 1 #Se for verdadeiro adiciona +1 na variável de número de linhas,
                    tabuleiro.pop(i) #Retira aquela linha do tabuleiro,
                    tabuleiro.insert(1,['!','0','0','0','0','0','0','0','0','0','0','!']) #E adiciona uma nova linha vazia no topo dele.
            pontuação = score(pontuação,n_linhas) #Adiciona pontuação de acordo com número de linhas eliminadas.
            #Verifica se a condição do while está verdadeira, para a musica, mostra mensagem de derrota.
            if f'{cor}1{Reset}' in tabuleiro[1]:
                pygame.mixer.music.stop() #para musica.
                clear()
                print(separador())
                print(texto_derrota.renderText('Game Over')) #mensagem de derrota.
                print(separador)
                time.sleep(3)
                clear()
    #Aumenta a dificuldade do jogo trocando o valor do tempo atraves de uma variavel dificuldade.
    elif função == '2':
        clear()
        conf = ''
        #while que so para de 'rodar quando uma dificuldade valida é escolhida.
        while conf != 'pronto':
            #Escolha da dificuldade.
            dificuldade = input(f'{"Qual dificuldade você quer jogar?":^100}\n'
                                f'{"[F] Fácil":^100}\n'
                                f'{"[M] Médio":^100}\n'
                                f'{"[I] Intermediário":^100}\n'
                                f'{"[D] Difícil":^100}\n'
                                f'{"[G] GOD OF TETRIS"}'
                                f'{"Responda e clique em enter: ":^100}').upper()
            #verifica se a dificuldade é valida e qual é ela, retonando um valor para cada uma.
            if dificuldade in ['F','M','I','D','G']:
                if dificuldade == 'F':
                    print('Dificuldade alterada para FÁCIL. Tempo de queda: 0.9 segundos.')
                    dificuldade = '1'
                elif dificuldade == 'M':
                    print('Dificuldade alterada para MÉDIO. Tempo de queda: 0.5 segundos.')
                    dificuldade = '2'
                elif dificuldade == 'I':
                    print('Dificuldade alterada para INTERMEDIÁRIO. Tempo de queda: 0.2 segundos.')
                    dificuldade = '3'
                elif dificuldade == 'D':
                    print('Dificuldade alterada para DIFÍCIL. Tempo de queda: 0.05 segundos.')
                    dificuldade = '4'
                elif dificuldade == 'G':
                    clear()
                    print('Mano, essa é a dificuldade GOD OF TETRIS! É um nível absurdo!')
                    confirmação = input('Certeza que deseja jogar na GOD OF TETRIS? [S/qualquer tecla] ').upper()
                    if confirmação == 'S':
                        print('VAI COM DEUS AMIGO!')
                        dificuldade = '5'
                    else:
                        print('Que bom que você tem juízo.')
                conf = 'pronto'
                time.sleep(1.5)
                clear()
            else:
                print('Digite apenas F,M, I, D ou G')
                time.sleep(1)
    #função que encerra o programa inteiro.
    elif função == '3':
        print('ENCERRANDO PROGRAMA!!')
        time.sleep(1)
        interface = 'Fechar'