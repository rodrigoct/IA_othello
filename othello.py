from threading import Thread
import sys
import time
from threading import Timer
import py_compile
py_compile.compile("othello.py")

EMPTY, BLACK, WHITE = '.', 'B', 'W'
PIECES = (EMPTY, BLACK, WHITE)
PLAYERS = {BLACK: 'Black', WHITE: 'White'}

# Direcao possivel
UP, DOWN, LEFT, RIGHT = -8, 8, -1, 1
NE, SE, SWE, NWE = -7, 9, 7, -9
DIRECTIONS = (UP, NE, RIGHT, SE, DOWN, SWE, LEFT, NWE)

'''

      0 1 2 3 4 5 6 7       0  1  2  3  4  5  6  7
    0 . . . . . . . .    0 00 01 02 03 04 05 06 07
    1 . . . . . . . .    1 08 09 10 11 12 13 14 15 
    2 . . . . . . . .    2 16 17 18 19 20 21 22 23
    3 . . . W B . . .    3 24 25 26 27 28 29 30 31
    4 . . . B W . . .    4 32 33 34 35 36 37 38 39
    5 . . . . . . . .    5 40 41 42 43 44 45 46 47
    6 . . . . . . . .    6 48 49 50 51 52 53 54 55
    7 . . . . . . . .    7 56 57 58 59 60 61 62 63

'''
TAB_VALORES = [

    160, -30,  30,   5,   5,  30, -30, 160,
    -30, -45,  -15,  -5,  -5,  -15, -45, -30,
    30,  -5,  15,   3,   3,  15,  -5,  30,
    10,  -5,   3,   3,   3,   3,  -5,   10,
    10,  -5,   3,   3,   3,   3,  -5,   10,
    30,  -5,  15,   3,   3,  15,  -5,  30,
    -30, -45,  -15,  -5,  -5,  -15, -45, -30,
    160, -30,  30,   5,   5,  30, -30, 160

]

'''TAB_VALORES = [

    120, -20,  20,   5,   5,  20, -20, 120,
    -20, -40,  -5,  -5,  -5,  -5, -40, -20,
    20,  -5,  15,   3,   3,  15,  -5,  20,
    5,  -5,   3,   3,   3,   3,  -5,   5,
    5,  -5,   3,   3,   3,   3,  -5,   5,
    20,  -5,  15,   3,   3,  15,  -5,  20,
    -20, -40,  -5,  -5,  -5,  -5, -40, -20,
    120, -20,  20,   5,   5,  20, -20, 120
]'''

class start_alfabeta(Thread):
    val = 0
    def __init__(self, tabuleiro, filho, cor, tempBase, profundidade):
        Thread.__init__(self)
        self.tabuleiro = tabuleiro[:]
        self.cor = cor
        self.filho = filho
        self.tempBase = tempBase
        self.profundidade = profundidade

    def run(self):
            #print "Nome da thread", self
            new_tab = self.tabuleiro
            cor = self.cor
            filho = self.filho
            profundidade = self.profundidade
            make_mov(new_tab, filho, cor)
            self.val = minimax_alfabeta(new_tab, profundidade, False, cor, oponente(cor), float('-infinity'), float('infinity'))
            #print "threadname retorna val", self.val, self
    def getFilhoValor(self):
        #print "Retorna getvalue"
        return self.val, self.filho          

def tabuleiro_init():
    """Cria o tabuleiro com o estado inicial do jogo"""
    tab = [EMPTY] * 64
    for i in range(0, 64):
        tab[i] = EMPTY

    # inicializa pecas do meio
    tab[27], tab[28] = WHITE, BLACK
    tab[35], tab[36] = BLACK, WHITE
    return tab


def play(tabuleiro, cor, torneio):
    global tempBase, tempLimit
    tempBase = time.time()
    pos_pecas = find_pecas(tabuleiro, cor)
    threads = []
    if(len(pos_pecas) == 0):
        print "GAME OVER"
        return -1
    
    filhos = find_filhos(tabuleiro, cor)

    if(len(filhos) == 0):
        print "Nao ha mov valido"
        return 0

    if(len(filhos) <= 2):
        profundidade = 10
        tempLimit = 3.5

    if(len(filhos) >= 3 and len(filhos) <= 5):
        profundidade = 6
        tempLimit = 2.7

    if(len(filhos) > 5 and len(filhos) < 8):
        profundidade = 5
        tempLimit = 2.7

    if(len(filhos) >= 8 and len(filhos) < 10):
        profundidade = 4
        tempLimit = 2.5

    if(len(filhos) >= 10):
        profundidade = 2
        tempLimit = 1.7

    if(len(filhos) >= 20):
        profundidade = 1
        tempLimit = 1.7
    bestValue = float('-infinity')
    val = bestValue
    filhoslist = []
    posMov = filhos[0]
    if(torneio):
        x = pos_x(posMov)
        y = pos_y(posMov)
        saida = open ( 'move.txt' , 'w' )
        saida.write(str(x) + "," + str(y))
    #print "Retorno da funcao filhos", filhos
    for filho in filhos:

        if((filho == 0 or filho == 7 or filho == 56 or filho == 63) and torneio):
            posMov = filho
            x = pos_x(posMov)
            y = pos_y(posMov)
            saida = open ( 'move.txt' , 'w' )
            saida.write(str(x) + "," + str(y))
            return 1

        thread = start_alfabeta(tabuleiro, filho, cor, tempBase, profundidade)
        threads.append(thread)
        thread.start()

    for th in threads:
        #print "threads", threads
        #print "nome da thread", th
        th.join()
        tupValFilho = th.getFilhoValor()
        val = tupValFilho[0]
        filho = tupValFilho[1]
        if (val > bestValue):
            bestValue = val
            posMov = filho
            #print "Achou um melhor", val, filho
        #print "valor retornado", val
        #a = raw_input("A")

    '''for val in valList:
            if (val > bestValue):
                bestValue = val
                posMov = filho
                print "Achou um melhor", val, filho'''
    #print "\n\nvalList", valList
    #print "time", time.time() - tempBase
    #a = raw_input("Faz mov:?")
    if(not torneio):
        make_mov(tabuleiro, posMov, cor)
    else:
        x = pos_x(posMov)
        y = pos_y(posMov)
        saida = open ( 'move.txt' , 'w' )
        saida.write(str(x) + "," + str(y))



def find_pecas(tabuleiro, cor):
    pos_pecas = []
    for i in range(0 ,64):
        if(tabuleiro[i] == cor):
            pos_pecas.append(i)
            #print i, tabuleiro[i]
    return pos_pecas

def tab_full(tabuleiro):
    for i in range(0 ,64):
        if(tabuleiro[i] == EMPTY):
            return False

    return True

def find_vizinhos(tabuleiro, pos_init, cor, k):
    vizinhos = {}
    tuplaret = ()
    for movs in DIRECTIONS:
        if(isValidMov(tabuleiro, pos_init, movs, cor)):
            nPos = pos_init + movs
            if (tabuleiro[nPos] == cor):
                tuplaret = mov_possiveis(tabuleiro, nPos, cor, movs)
                #print tuplaret
                vizinhos[str(k)] = {"pos_fin": tuplaret[0], "npecas" : tuplaret[1]}
                k = k + 1

    return vizinhos

def find_filhos(tabuleiro, cor):

    vizinhos = {}
    filhos = []
    k = 0
    max_value = 0
    cor_inv = oponente(cor)
    pos_pecas = find_pecas(tabuleiro, cor)

    #Verfica direcoes do vizinho
    for pos in pos_pecas:
        dicio = find_vizinhos(tabuleiro, pos, cor_inv, k)
        for key, value in dicio.iteritems():
            vizinhos[key] = value
            if(int(key) > max_value):
                max_value = int(key)

        k = max_value + 1
    #print "Vizinhos da cor", cor, vizinhos
    for key, value in vizinhos.iteritems():
        if( (not filhos.__contains__(value['pos_fin']))  and value['npecas'] != 0):
            filhos.append(value['pos_fin'])

    return filhos

#board
def isInsideBoard(tab, pos, movs):
    if (pos + movs >= 0 and pos + movs < 64):
        return True
    return False

#board e cor da peca
def isValidMov(tab, pos, movs, cor):
    x = pos_x(pos)
    y = pos_y(pos)
    if (pos + movs >= 0 and pos + movs < 64):

        if( (movs == LEFT) and x == 0):
            return False
        if( (movs == RIGHT) and x == 7):
            return False
        if( (movs == NE or movs == SE) and x == 7):
            return False
        if( (movs == NWE or movs == SWE) and x == 0):
            return False

        if(tab[pos + movs] == cor or tab[pos + movs] == EMPTY):
            return True

    return False

def isSeqOp(tab, pos, movs, cor):
    x = pos_x(pos)
    y = pos_y(pos)   
    if (pos + movs >= 0 and pos + movs < 64):

        if( (movs == LEFT) and x == 0):
            return False
        if( (movs == RIGHT) and x == 7):
            return False
        if( (movs == NE or movs == SE) and x == 7):
            return False
        if( (movs == NWE or movs == SWE) and x == 0):
            return False

        if(tab[pos + movs] == cor):
            return True    
    return False

def oponentes_seq(tab, pos, cor, movs):
    nPos = pos
    pos_reversi = []
    pos_reversi.append(pos)
    while (tab[nPos] != EMPTY):
        if(isSeqOp(tab, nPos, movs, cor)):
            nPos = nPos + movs
            pos_reversi.append(nPos)

        else:
                #if(isInsideBoard(tab, nPos, movs)):
                if(isSeqOp(tab, nPos, movs, oponente(cor))):
                    #if (tab[nPos + movs] == oponente(cor)): 
                    return pos_reversi
                else:
                    pos_reversi = []
                    return pos_reversi
                pos_reversi = []
                return pos_reversi

    return pos_reversi

def oponente(player):
    
    return BLACK if player is WHITE else WHITE

def mov_possiveis(tab, pos, cor, movs):
    nPos = pos
    qnt_pecas = 1
    while (tab[nPos] != EMPTY):
        if(isValidMov(tab, nPos, movs, cor)):
            nPos = nPos + movs
        else:
            return pos, 0
    return nPos, qnt_pecas


def minimax_alfabeta(tab, profundidade, maxPlayer, corInit, cor, alfa, beta):
    new_tab = tab[:]
    timeC = time.time() - tempBase
    if (timeC > tempLimit):
        #print "Tempo expirou ", profundidade
        return heuristica(tab, corInit)
    if profundidade == 0 or tab_full(tab):
        if(tab_full(tab)):
            tup = conta_pecas(tab)
            if (corInit == BLACK):
                if(tup[0] > 32):
                    return 1000
            else:
                if(tup[1] > 32):
                    return 1000

        return heuristica(tab, corInit)
    if maxPlayer:
        filhos = find_filhos(new_tab, cor)
        op_cor = oponente(cor)
        for filho in filhos:
            new_tab = tab[:]
            make_mov(new_tab, filho, cor)
            alfa = max(alfa, minimax_alfabeta(new_tab, profundidade - 1, False, corInit, op_cor, alfa, beta))
            if (beta <= alfa):
                break
        return alfa
    else:
        filhos = find_filhos(new_tab, cor)
        op_cor = oponente(cor)
        for filho in filhos:
            new_tab = tab[:]
            make_mov(new_tab, filho, cor)
            beta = min(beta, minimax_alfabeta(new_tab, profundidade - 1, True, corInit, op_cor, alfa,beta))
            if (beta <= alfa):
                break
        return beta

def heuristica(tabuleiro, cor):
    #print "qntd de pecas ", len(find_pecas(tabuleiro, cor))
    val = 0
    Valores_locais = TAB_VALORES[:]
    pos_pecas_cor = find_pecas(tabuleiro, cor)
    pos_pecas_op = find_pecas(tabuleiro, oponente(cor))

    if(tabuleiro[0] == cor):
        Valores_locais[1] = 50
        Valores_locais[8] = 50
        Valores_locais[9] = 10
    if(tabuleiro[7] == cor):
        Valores_locais[6] = 50
        Valores_locais[15] = 50
        Valores_locais[14] = 10
    if(tabuleiro[56] == cor):
        Valores_locais[48] = 50
        Valores_locais[57] = 50
        Valores_locais[49] = 10
    if(tabuleiro[63] == cor):
        Valores_locais[55] = 50
        Valores_locais[62] = 50
        Valores_locais[54] = 10

    if(tabuleiro[0] == oponente(cor)):
        Valores_locais[1] = -40
        Valores_locais[8] = -40
        Valores_locais[9] = -60
    if(tabuleiro[7] == oponente(cor)):
        Valores_locais[6] = -40
        Valores_locais[15] = -40
        Valores_locais[14] = -60
    if(tabuleiro[56] == oponente(cor)):
        Valores_locais[48] = -40
        Valores_locais[57] = -40
        Valores_locais[49] = -60
    if(tabuleiro[63] == oponente(cor)):
        Valores_locais[55] = -40
        Valores_locais[62] = -40
        Valores_locais[54] = -60

    for i in pos_pecas_cor:
        val = val + Valores_locais[i]
    for i in pos_pecas_op:
        val = val - TAB_VALORES[i]

    return val

def make_mov(tab, pos, cor):
    new_tab = tab[:]
    op = oponente(cor)
    pos_reversi = []
    for movs in DIRECTIONS:
        if(isSeqOp(new_tab, pos, movs, op)):
            pos_reversi = oponentes_seq(new_tab, pos + movs, op, movs)
            for invert in pos_reversi:
                tab[invert] = cor
    tab[pos] = cor
    
def print_board(tabuleiro):
    print "Imprimindo tabuleiro"
    print "  0.1.2.3.4.5.6.7" 
    for i in range(0,8):
        print i, (" ".join(tabuleiro[i*8 : i*8 + 8]))

def pos_x(pos):
    x = pos % 8
    return x

def pos_y(pos):
    y = pos / 8
    return y

def pos_tab(x, y):
    pos = x + 8*y
    return pos 

def human(tab, cor):

    print "Posicoes possiveis"
    pos_pecas = find_pecas(tab, cor)
    if(len(pos_pecas) == 0):
        print "GAME OVER"
        return -1

    filhos = find_filhos(tab, cor)

    if(len(filhos) == 0):
        print "Nao ha mov valido"
        return 0

    '''for pos_possiveis in filhos:
        #print pos_possiveis
        x = pos_x(pos_possiveis)
        y = pos_y(pos_possiveis)
        pos = pos_tab(x, y)
        print "Posicoes possiveis x",x, "y",y'''
    while(True):
        x = raw_input('Digite x ')
        y = raw_input('Digite y ')
        int_control = True

        for i in x:
            if(i.isalpha()):
                int_control = False
                break
        for i in y:
            if(i.isalpha()):
                int_control = False
                break

        if(len(x) == 0 or len(y) == 0):
                int_control = False

        if(not(int_control)):
            print "Formato invalido, digite novamente"

        else:
            go_x = int(x)
            go_y = int(y)
            go_pos = pos_tab(go_x, go_y)
            if(filhos.__contains__(go_pos)):
                make_mov(tab, go_pos, cor)
                break
            else:
                print "Movimento invalido"


def conta_pecas(tabuleiro):
    #print "qntd de pecas ", len(find_pecas(tabuleiro, cor))
    n_blacks = 0
    n_whites = 0
    pos_pecas_b = find_pecas(tabuleiro, BLACK)
    pos_pecas_w = find_pecas(tabuleiro, WHITE)

    for i in pos_pecas_b:
        n_blacks = n_blacks + 1
    for i in pos_pecas_w:
        n_whites = n_whites +1

    return n_blacks, n_whites

def ler_tab(narquivo):
    tab = [EMPTY] * 64
    i = 0
    arquivo = file(narquivo,'r')
    linhas = arquivo.readlines()
    for linha in linhas:
        tab[i*8 : i*8 + 8] = linha[0:8]
        i = i + 1

    return tab

def player_cor(nome):
    if (nome == "black"):
        cor = BLACK
    else:
        cor = WHITE

    return cor

def main(cmd_args):
    count = 0
    if (len(cmd_args) == 0):
        tab = tabuleiro_init()
        #while(not tab_full(tab) and count <= 2):
        while(not tab_full(tab)):
            cor = BLACK
            count = count + 1
            print_board(tab)
            cor_op = oponente(cor)
            enable_human = human(tab, cor)
            #enable_human = play(tab, cor, False)
            if(enable_human == -1):
                print "GAME OVER"
                break
            print_board(tab)
            print "PENSANDO"
            enable_play = play(tab, cor_op, False)
            if(enable_play == -1):
                print "GAME OVER"
                break
            print "Retorno human e play", enable_human, enable_play
            if(enable_human == 0 and enable_play == 0):
                print "GAME OVER NAO HA MOVS POSSIVEIS"
                break

    else:
        cor = player_cor(cmd_args[1])
        tab = ler_tab(cmd_args[0])
        enable_play = play(tab, cor, True)
        if(enable_play == 0):
            print "NAO HA MOVS POSSIVEIS"
            saida = open ( 'move.txt' , 'w' )
            saida.write("-1,-1")

'''
    print_board(tab)
    print "Verifica vencedor"
    tup = conta_pecas(tab)
    print "Pecas pretas ", tup[0],"Pecas brancas", tup[1]'''

if __name__ == '__main__':
    main(sys.argv[1:]) 