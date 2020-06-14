# -*- coding: utf-8 -*-

import os
import pandas as pd


def prepare_df(filename='saojoao.txt'):
    try:        # Tenta carregar os dados de um arquivo ja existente
        df = pd.read_csv(filename, sep=";");
        print (df.head())
    except:     # Se der erro, ele cria um novo set de dados (primeira vez)
        df = pd.DataFrame(columns=["nome"]);
    return df

def filter_arqs(cols, localpath='.'):
    # Essa funcao compara as colunas ja existentes no CSV com os arquivos txt que estao na pasta.
    # E retorna quais arquivos ainda não foram processados.
    for i in range(len(cols)):
        cols[i]=cols[i][-2:]

    arquivos=os.listdir(localpath)
    arqs=[]

    for arquivo in arquivos:
        if (arquivo[-4:] == '.txt'):
            if arquivo[:2] not in cols:
                arqs.append(arquivo);
    return arqs

def load_new_votos(df, filename, path='./'):
    # Essa funcao pega cada arquivo e faz a distribuicao dos votos

    # Baseia-se no nome do arquivo para distribuir os votos em cada partida

    #partida = "Jogo"+filename[:2]
    partida = filename[0:-4]

    try:
        df.insert(1,partida,0)
    except:
        pass;

    with open(path+filename) as f:
        #votantes = f.readlines();
        lines = f.readlines();

        for line in lines:
            lineSplit=line.split(";")
            pessoa = lineSplit[0]
            voto = lineSplit[1].replace("\n",'')
            if (pessoa != '' and pessoa!='\n'):    # ignorar linhas vazias
                # procurar pessoa no df. Se nao achar, cria-la
                if len(df.loc[(df.nome==pessoa)])==0:
                    df = df.append({'nome':pessoa, partida:voto}, ignore_index=True);
                # aumentar pontuacao dela.
                df.loc[(df.nome == pessoa),partida]=voto
    return df


# Carrega o arquivo de votação já existente ou cria um novo
df = prepare_df();

# Obtem os arquivos ainda nao processados
arquivos = filter_arqs(list(df.columns)); # Aqui eu especifiquei a pasta com os txts (mas se tiver na raiz nao precisa)

for arquivo in arquivos:
    df = load_new_votos(df, arquivo);   # Aqui eu especifiquei a pasta com os txts (mas se tiver na raiz nao precisa)

df.to_csv('saojoao.csv', sep= ';', index=False)

