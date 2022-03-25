import pickle
import time
import operator

time1 = time.time()

list_trajectory = []                        # vetor de listas que contem as trajetorias
i_x = 0                                     # incrementar chave de dict_x
n = 12                       # numero celulas na sequencia
n_window = 1                                # numero de celulas que desliza a janela

outputs = 4

states = []                         # vetor de estados
emit_p = {}                         # dicionario emissions
trans_p = {}                        # dicionario transitions
start_p = {}
seqs_firstCells = {}

sorted_seq = []
cum_prob_dict = {}

######################################################################################

def seq_ident(seq):                 # funcao que identa sequencias: retorna a string sequencia por exemplo 03030303
    seq_aux = []
    for cell in seq:                # percorre cada celula da sequencia
        if len(cell) == 1:          # quando a celula tem so 1 caracter adiciona 0
            cell_aux = '00' + cell
        elif len(cell) == 2:
            cell_aux = '0' + cell
        else:                       # caso contrario a celula mantem-se igual
            cell_aux = cell

        seq_aux.append(cell_aux)    # adiciona a celula ja modificada a uma seq_aux

    str1 = ''.join(seq_aux)          # string sequencia

    return str1

#########################################################################################

def states_prob(seq_aux):
    if seq_aux not in states:       # se a sequencia ainda nao estiver nos estados atualiza
        states.append(seq_aux)

#########################################################################################
def initial_prob(seq_aux):
    if seq_aux not in start_p:
        start_p[seq_aux] = 1

    else:
        start_p[seq_aux] += 1

#########################################################################################
def emit_prob(seq,seq_aux):
    if seq_aux not in emit_p:           # verifica se o dicionario emission tem a sequencia
        emit_p[seq_aux] = {}            # se nao tem adiciona uma nova entrada com a chave seq_aux
        for item in seq:
            if item in emit_p[seq_aux]:
                emit_p[seq_aux][item] += 1/n
            else:
                emit_p[seq_aux][item] = 1/n

#########################################################################################
def trans_prob(seq_aux):
    if seq_aux not in trans_p:
        trans_p[seq_aux] = {}

    if len(l_aux)>1:
        if seq_aux in trans_p[l_aux[-2]]:
            trans_p[l_aux[-2]][seq_aux] += 1
        else:
            trans_p[l_aux[-2]][seq_aux] = 1

########################################################################################
def update_initial():
    counter = 0
    for key in start_p:
        counter += start_p[key]

    for key in start_p:
        start_p[key] = start_p[key]/counter


########################################################################################
def update_trans():
    for key in trans_p:
        counter = 0
        for item in trans_p[key]:
            counter += trans_p[key][item]

        for item in trans_p[key]:
            trans_p[key][item] = trans_p[key][item]/counter

#########################################################################################
#########################################################################################
def sort_sequences():
    sorted_d = dict(sorted(start_p.items(), key=operator.itemgetter(1),reverse=True))

    cum_sum = 0
    for seq in sorted_d:
        cum_sum += sorted_d[seq]
        cum_prob_dict[seq] = cum_sum
        sorted_seq.append(seq)

##########################################################################################

def add_dict_firstCells(seq_aux):

    chars = 3*(n-outputs)
    first_cells = seq_aux[0:chars]

    allSeqs = []

    if first_cells not in seqs_firstCells:           # verifica se o dicionario emission tem a sequencia
        allSeqs.append(seq_aux)
        seqs_firstCells[first_cells] = allSeqs


    else:
         allSeqs = seqs_firstCells.get(first_cells)

         if seq_aux not in allSeqs:
            allSeqs.append(seq_aux)

         seqs_firstCells[first_cells] = allSeqs



#################################   MAIN  ###################################################


with open("MUNSTER256.txt") as file:

    for line in file:
        line = line.strip()                 #vai ler cada linha do trajectory
        t = line.split(" ")                 # converte a string da linha numa lista

        if len(t) >= n:                     # verifica se a trajectoria tem mais que n celulas
            list_trajectory.append(t)

count_samples = 0
count = 0

# for i in list_trajectory:
#     for j in i:
#         if j == "71" or j == "57":
#              count+=1

# print(count)


for item in list_trajectory:
    l = [item[i:i + n] for i in range(0, len(item), n_window)]  # divide cada trajetoria em sequencias de n celulas
    l_aux=[]


    for seq in l:                                       # percorre cada sequencia que resulta da divisao
        if len(seq) == n:                               # verifica se tem n celulas
            seq_aux = seq_ident(seq)                    # sequenciaa identada
            l_aux.append(seq_aux)                       # coloca a sequencia aux numa lista
            states_prob(seq_aux)                  # testa e se nao existir adiciona a sequencia ao vetor states
            add_dict_firstCells(seq_aux)          # adiciona ao dict que tem as sequencias identicas nas n-1 celulas
            emit_prob(seq,seq_aux)                #teste e se nao existir adiciona entrada na tabela emission
            trans_prob(seq_aux)                   # adiciona sequencia a matriz transicao e atualiza contadores
            initial_prob(seq_aux)
            count_samples += 1


update_initial()
update_trans()
sort_sequences()


print("SCENARIO: n=%s w=%s" % (n,n_window))
print("Different sequences:", len(states))
print("Observation space:", count_samples)


elapsed = time.time() - time1
print(elapsed)

file_array = [trans_p, emit_p, start_p, states, sorted_seq, seqs_firstCells, cum_prob_dict]
file_name = ['transition_prob', 'emission_prob', 'initial_prob', 'states_info', 'sorted_Seq', 'seqs_First', 'sequences_cum_prob']
file_counter = 0

for file in file_array:
    f = open(file_name[file_counter]+'.pkl', "wb")  # save the probabilities on files
    pickle.dump(file, f)
    f.close()
    file_counter += 1

