# from collector import prepare_rdf
import pandas as pd
import sys

def build_mdf(rdf):
    votantes=[]
    for i in range(rdf.shape[0]):
        votantes.append(rdf.iloc[i].nome);
    mdf = pd.DataFrame(index=votantes, columns=votantes)
    return mdf

def match_evaluation(rdf, mdf):
    cols = list(rdf.columns)
    for i in range(rdf.shape[0]-1):
        p1 = rdf.iloc[i]['nome']
        print(p1)
        for j in range(i+1,rdf.shape[0]-1):
            p2 = rdf.iloc[j]['nome']
            #print (p1,"vs", p2)
            both_voted=0;
            matched=0;
            for k in range(1,len(cols)):
                if (rdf.iloc[i][cols[k]] != None) and (rdf.iloc[i][cols[k]] != 0) and (rdf.iloc[j][cols[k]] != None) and (rdf.iloc[j][cols[k]] != 0):
                    both_voted+=1
                    if (rdf.iloc[i][cols[k]] == rdf.iloc[j][cols[k]]):
                        matched+=1;
            mdf[p1][p2]=round(100*float(matched)/float(both_voted),2)
            mdf[p2][p1]=round(100*float(matched)/float(both_voted),2)
            #float(matched)/float(both_voted)

#df = pd.read_csv("docinhos_filtro.csv", sep=",");
file = sys.argv[1]
df = pd.read_csv(file, delimiter=";");
mdf = build_mdf(df)
match_evaluation(df, mdf)
mdf.to_csv('saojoao_match.csv', sep= ';', index=True)