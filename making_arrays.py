import pickle
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import re
import time
from sklearn import tree

player_stats = pd.read_csv("player_stats.csv")

teams = {"liverpool":['S. MANÉ','ROBERTO FIRMINO','M. SALAH','N. KEÏTA','G. WIJNALDUM','J. HENDERSON','A. ROBERTSON','V. VAN DIJK','D. LOVREN','T. A. ARNOLD'],
"barcelona":['A. GRIEZMANN','L. SUÁREZ','L. MESSI','F. DE JONG','I. RAKITIĆ','SERGI ROBERTO','JORDI ALBA','C. LENGLET','PIQUÉ','NÉLSON SEMEDO'], "manchester_city":['R. STERLING','S. AGÜERO','L. SANÉ','BERNARDO SILVA','FERNANDINHO','İ. GÜNDOĞAN','B. MENDY','V. KOMPANY','J. STONES','K. WALKER'],
"bayern_munchen":['J. RODRÍGUEZ','R. LEWANDOWSKI','THIAGO A.','P. COUTINHO','T. MÜLLER','L. GORETZKA','D. ALABA','M. HUMMELS','J. BOATENG','J. KIMMICH'],
"juventus":['DOUGLAS COSTA','C. RONALDO','P. DYBALA','B. MATUIDI','M. PJANIĆ','S. KHEDIRA','L. SPINAZZOLA','G. CHIELLINI','L. BONUCCI','JOÃO CANCELO'],
"ajax":['D. TADIĆ','Q. PROMES','D. VAN DE BEEK','H. ZIYECH','DAVID NERES','É. ÁLVAREZ','N. TAGLIAFICO','D. BLIND','J. VELTMAN','N. MAZRAOUI'],"psg":["NEYMAR","E. CAVANI","K. MBAPPÉ","M. VERRATTI","L. PAREDES","A. RABIOT","L. KURZAWA","THIAGO SILVA","MARQUINHOS","DANI ALVES"],
"real_madrid":["VINÍCIUS JÚNIOR","K. BENZEMA","G. BALE","L. MODRIĆ","CASEMIRO","ISCO","MARCELO","SERGIO RAMOS","R. VARANE","DANIEL CARVAJAL"],
"flamengo:":["M. MORENO","F. URIBE","GEUVÂNIO","R. PIRIS","WILLIAN ARÃO","DIEGO","RENÊ","LÉO DUARTE","RHODOLFO","RODINEI"],
"atletico_madrid":["N. KALINIĆ","DIEGO COSTA","VITOLO","SAÚL","T. PARTEY","KOKE","FILIPE LUIS","D. GODÍN","L. HERNANDEZ","S. ARIAS"],
"inter_milan":["H. ÇALHANOĞLU","K. PIĄTEK","SUSO","G. BONAVENTURA","L. BIGLIA","LUCAS PAQUETÁ","R. RODRÍGUEZ","A. ROMAGNOLI","M. CALDARA","D. CALABRIA"],
"benfica":["F. CERVI","H. SEFEROVIĆ","E. SALVIO","PIZZI","L. FEJSA","GABRIEL PIRES","ÁLEX GRIMALDO","RÚBEN DIAS","G. CONTI","ANDRÉ ALMEIDA"],
"fc_porto":["V. ABOUBAKAR","J. CORONA","TIQUINHO SOARES","H. HERRERA","DANILO PEREIRA","Y. BRAHIMI","ALEX TELLES","FELIPE","PEPE","M. PEREIRA"],
"chelsea":["E. HAZARD","G. HIGUAÍN","WILLIAN","N. KANTÉ","JORGINHO","R. BARKLEY","MARCOS ALONSO","A. RÜDIGER","DAVID LUIZ","AZPILICUETA"],
"atalanta":["D. ZAPATA","R. GOSENS","H. HATEBOER","M. DE ROON","R. FREULER","J. ILIČIĆ","RAFAEL TOLÓI","A. MASIELLO","J. PALOMINO","G. MANCINI"],
"valencia":["SANTI MINA","GONÇALO GUEDES","RODRIGO","D. CHERYSHEV","G. KONDOGBIA","DANI PAREJO","JOSÉ GAYÁ","E. GARAY","GABRIEL","C. PICCINI"],
"shakhtar_donetsk":["O. KAYODE","JÚNIOR MORAES","MARLOS","MAYCON","T. STEPANENKO","TAISON","ISMAILY","I. ORDETS","S. KRIVTSOV","B. BUTKO"],
"roma":["D. PEROTTI","E. DŽEKO","C. ÜNDER","L. PELLEGRINI","D. DE ROSSI","J. PASTORE","A. KOLAROV","K. MANOLAS","F. FAZIO","A. FLORENZI"],
"leicester_city":["M. ALBRIGHTON","J. VARDY","K. IHEANACHO","Y. TIELEMANS","W. NDIDI","J. MADDISON","B. CHILWELL","H. MAGUIRE","J. EVANS","RICARDO PEREIRA"],
"sevilla":["L. OCAMPOS","L. DE JONG","RONY LOPES","N. GUDELJ","FERNANDO","É. BANEGA","ESCUDERO","DIEGO CARLOS","DANIEL CARRIÇO","SERGI GÓMEZ"],
"lazio":["M. PAROLO","C. IMMOBILE","F. CAICEDO","S. M. SAVIĆ","LUCAS LEIVA","LUIS ALBERTO","J. LUKAKU","F. ACERBI","WALLACE","D. BASTA"],
"napoli":["L. INSIGNE","D. MERTENS","JOSÉ CALLEJÓN","ALLAN","P. ZIELIŃSKI","FABIÁN RUIZ","F. GHOULAM","K. KOULIBALY","ALBIOL","K. MALCUIT"],
"getafe":["JAIME MATA","ÁNGEL","G. SHIBASAKI","N. MAKSIMOVIĆ","BERGARA","BERGARA","V. ANTUNES","D. DAKONAM","BRUNO","D. SUÁREZ"],
"tottenham":["SON HEUNG-MIN","H. KANE","LUCAS MOURA","D. ALLI","E. DIER","C. ERIKSEN","D. ROSE","T. ALDERWEIRELD","J. VERTONGHEN","K. TRIPPIER"],
"manchester_united":["A. SÁNCHEZ","R. LUKAKU","J. LINGARD","P. POGBA","N. MATIĆ","FRED","L. SHAW","E. BAILLY","P. JONES","A. VALENCIA"],
"boca_juniors":["R. ÁBILA","D. BENEDETTO","C. PAVÓN","N. NÁNDEZ","I. MARCONE","E. REYNOSO","F. FABRA","C. IZQUIERDOZ","P. GOLTZ","J. BUFFARINI"]}


def get_team(playername):
    for team in teams:
        if playername in teams[team]:
            return team


player_stats['team'] = player_stats['Name:'].apply(lambda x: get_team(x))
numbers_stats = player_stats[['Attacking Prowess:','Ball Control:','Dribbling:','Low Pass:','Lofted Pass:','Finishing:','Place Kicking:','Swerve:','Header:','Defensive Prowess:','Ball Winning:','Kicking Power:','Speed:','Explosive Power:','Unwavering Balance:','Physical Contact:','Jump:','Stamina:']]

player_array = numbers_stats.to_numpy()

barcelona_matrix = player_stats.loc[player_stats['team'] == 'barcelona']
barcelona_matrix = barcelona_matrix[['Attacking Prowess:','Ball Control:','Dribbling:','Low Pass:','Lofted Pass:','Finishing:','Place Kicking:','Swerve:','Header:','Defensive Prowess:','Ball Winning:','Kicking Power:','Speed:','Explosive Power:','Unwavering Balance:','Physical Contact:','Jump:','Stamina:']].to_numpy()
sampledata = [barcelona_matrix.flatten()]

liverpool_matrix = player_stats.loc[player_stats['team'] == 'liverpool']
liverpool_matrix = liverpool_matrix[['Attacking Prowess:','Ball Control:','Dribbling:','Low Pass:','Lofted Pass:','Finishing:','Place Kicking:','Swerve:','Header:','Defensive Prowess:','Ball Winning:','Kicking Power:','Speed:','Explosive Power:','Unwavering Balance:','Physical Contact:','Jump:','Stamina:']].to_numpy()
sampledata1 = [liverpool_matrix.flatten()]
sampledata = np.append(sampledata, sampledata1, axis=0)

ajax_matrix = player_stats.loc[player_stats['team'] == 'ajax']
ajax_matrix = ajax_matrix[['Attacking Prowess:','Ball Control:','Dribbling:','Low Pass:','Lofted Pass:','Finishing:','Place Kicking:','Swerve:','Header:','Defensive Prowess:','Ball Winning:','Kicking Power:','Speed:','Explosive Power:','Unwavering Balance:','Physical Contact:','Jump:','Stamina:']].to_numpy()
sampledata2 = [ajax_matrix.flatten()]
sampledata = np.append(sampledata, sampledata2, axis=0)

bayern_matrix = player_stats.loc[player_stats['team'] == 'bayern_munchen']
bayern_matrix = bayern_matrix[['Attacking Prowess:','Ball Control:','Dribbling:','Low Pass:','Lofted Pass:','Finishing:','Place Kicking:','Swerve:','Header:','Defensive Prowess:','Ball Winning:','Kicking Power:','Speed:','Explosive Power:','Unwavering Balance:','Physical Contact:','Jump:','Stamina:']].to_numpy()
sampledata3 = [bayern_matrix.flatten()]
sampledata = np.append(sampledata, sampledata3, axis=0)

manchester_city_matrix = player_stats.loc[player_stats['team'] == 'manchester_city']
manchester_city_matrix = manchester_city_matrix[['Attacking Prowess:','Ball Control:','Dribbling:','Low Pass:','Lofted Pass:','Finishing:','Place Kicking:','Swerve:','Header:','Defensive Prowess:','Ball Winning:','Kicking Power:','Speed:','Explosive Power:','Unwavering Balance:','Physical Contact:','Jump:','Stamina:']].to_numpy()
sampledata4 = [manchester_city_matrix.flatten()]
sampledata = np.append(sampledata, sampledata4, axis=0)

juventus_matrix = player_stats.loc[player_stats['team'] == 'juventus']
juventus_matrix = juventus_matrix[['Attacking Prowess:','Ball Control:','Dribbling:','Low Pass:','Lofted Pass:','Finishing:','Place Kicking:','Swerve:','Header:','Defensive Prowess:','Ball Winning:','Kicking Power:','Speed:','Explosive Power:','Unwavering Balance:','Physical Contact:','Jump:','Stamina:']].to_numpy()
sampledata5 = [juventus_matrix.flatten()]
sampledata = np.append(sampledata, sampledata5, axis=0)

psg_matrix = player_stats.loc[player_stats['team'] == 'psg']
psg_matrix = psg_matrix[['Attacking Prowess:','Ball Control:','Dribbling:','Low Pass:','Lofted Pass:','Finishing:','Place Kicking:','Swerve:','Header:','Defensive Prowess:','Ball Winning:','Kicking Power:','Speed:','Explosive Power:','Unwavering Balance:','Physical Contact:','Jump:','Stamina:']].to_numpy()
sampledata6 = [psg_matrix.flatten()]
sampledata = np.append(sampledata, sampledata6, axis=0)

real_madrid_matrix = player_stats.loc[player_stats['team'] == 'real_madrid']
real_madrid_matrix = real_madrid_matrix[['Attacking Prowess:','Ball Control:','Dribbling:','Low Pass:','Lofted Pass:','Finishing:','Place Kicking:','Swerve:','Header:','Defensive Prowess:','Ball Winning:','Kicking Power:','Speed:','Explosive Power:','Unwavering Balance:','Physical Contact:','Jump:','Stamina:']].to_numpy()
sampledata7 = [real_madrid_matrix.flatten()]
sampledata = np.append(sampledata, sampledata7, axis=0)

# flamengo_matrix = player_stats.loc[player_stats['team'] == 'flamengo']
# print(flamengo_matrix)
# flamengo_matrix = flamengo_matrix[['Attacking Prowess:','Ball Control:','Dribbling:','Low Pass:','Lofted Pass:','Finishing:','Place Kicking:','Swerve:','Header:','Defensive Prowess:','Ball Winning:','Kicking Power:','Speed:','Explosive Power:','Unwavering Balance:','Physical Contact:','Jump:','Stamina:']].to_numpy()
# sampledata8 = [flamengo_matrix.flatten()]
# sampledata = np.append(sampledata, sampledata8, axis=0)

atletico_madrid_matrix = player_stats.loc[player_stats['team'] == 'atletico_madrid']
atletico_madrid_matrix = atletico_madrid_matrix[['Attacking Prowess:','Ball Control:','Dribbling:','Low Pass:','Lofted Pass:','Finishing:','Place Kicking:','Swerve:','Header:','Defensive Prowess:','Ball Winning:','Kicking Power:','Speed:','Explosive Power:','Unwavering Balance:','Physical Contact:','Jump:','Stamina:']].to_numpy()
sampledata9 = [atletico_madrid_matrix.flatten()]
sampledata = np.append(sampledata, sampledata9, axis=0)

inter_milan_matrix = player_stats.loc[player_stats['team'] == 'inter_milan']
inter_milan_matrix = inter_milan_matrix[['Attacking Prowess:','Ball Control:','Dribbling:','Low Pass:','Lofted Pass:','Finishing:','Place Kicking:','Swerve:','Header:','Defensive Prowess:','Ball Winning:','Kicking Power:','Speed:','Explosive Power:','Unwavering Balance:','Physical Contact:','Jump:','Stamina:']].to_numpy()
sampledata10 = [inter_milan_matrix.flatten()]
sampledata = np.append(sampledata, sampledata10, axis=0)

benfica_matrix = player_stats.loc[player_stats['team'] == 'benfica']
benfica_matrix = benfica_matrix[['Attacking Prowess:','Ball Control:','Dribbling:','Low Pass:','Lofted Pass:','Finishing:','Place Kicking:','Swerve:','Header:','Defensive Prowess:','Ball Winning:','Kicking Power:','Speed:','Explosive Power:','Unwavering Balance:','Physical Contact:','Jump:','Stamina:']].to_numpy()
sampledata11 = [benfica_matrix.flatten()]
sampledata = np.append(sampledata, sampledata11, axis=0)

fc_porto_matrix = player_stats.loc[player_stats['team'] == 'fc_porto']
fc_porto_matrix = fc_porto_matrix[['Attacking Prowess:','Ball Control:','Dribbling:','Low Pass:','Lofted Pass:','Finishing:','Place Kicking:','Swerve:','Header:','Defensive Prowess:','Ball Winning:','Kicking Power:','Speed:','Explosive Power:','Unwavering Balance:','Physical Contact:','Jump:','Stamina:']].to_numpy()
sampledata12 = [fc_porto_matrix.flatten()]
sampledata = np.append(sampledata, sampledata12, axis=0)

chelsea_matrix = player_stats.loc[player_stats['team'] == 'chelsea']
chelsea_matrix = chelsea_matrix[['Attacking Prowess:','Ball Control:','Dribbling:','Low Pass:','Lofted Pass:','Finishing:','Place Kicking:','Swerve:','Header:','Defensive Prowess:','Ball Winning:','Kicking Power:','Speed:','Explosive Power:','Unwavering Balance:','Physical Contact:','Jump:','Stamina:']].to_numpy()
sampledata13 = [chelsea_matrix.flatten()]
sampledata = np.append(sampledata, sampledata13, axis=0)

atalanta_matrix = player_stats.loc[player_stats['team'] == 'atalanta']
atalanta_matrix = atalanta_matrix[['Attacking Prowess:','Ball Control:','Dribbling:','Low Pass:','Lofted Pass:','Finishing:','Place Kicking:','Swerve:','Header:','Defensive Prowess:','Ball Winning:','Kicking Power:','Speed:','Explosive Power:','Unwavering Balance:','Physical Contact:','Jump:','Stamina:']].to_numpy()
sampledata14 = [atalanta_matrix.flatten()]
sampledata = np.append(sampledata, sampledata14, axis=0)

valencia_matrix = player_stats.loc[player_stats['team'] == 'valencia']
valencia_matrix = valencia_matrix[['Attacking Prowess:','Ball Control:','Dribbling:','Low Pass:','Lofted Pass:','Finishing:','Place Kicking:','Swerve:','Header:','Defensive Prowess:','Ball Winning:','Kicking Power:','Speed:','Explosive Power:','Unwavering Balance:','Physical Contact:','Jump:','Stamina:']].to_numpy()
sampledata15 = [valencia_matrix.flatten()]
sampledata = np.append(sampledata, sampledata15, axis=0)

shakhtar_donetsk = player_stats.loc[player_stats['team'] == 'shakhtar_donetsk']
shakhtar_donetsk = shakhtar_donetsk[['Attacking Prowess:','Ball Control:','Dribbling:','Low Pass:','Lofted Pass:','Finishing:','Place Kicking:','Swerve:','Header:','Defensive Prowess:','Ball Winning:','Kicking Power:','Speed:','Explosive Power:','Unwavering Balance:','Physical Contact:','Jump:','Stamina:']].to_numpy()
sampledata16 = [shakhtar_donetsk.flatten()]
sampledata = np.append(sampledata, sampledata16, axis=0)

roma_matrix = player_stats.loc[player_stats['team'] == 'roma']
roma_matrix = roma_matrix[['Attacking Prowess:','Ball Control:','Dribbling:','Low Pass:','Lofted Pass:','Finishing:','Place Kicking:','Swerve:','Header:','Defensive Prowess:','Ball Winning:','Kicking Power:','Speed:','Explosive Power:','Unwavering Balance:','Physical Contact:','Jump:','Stamina:']].to_numpy()
sampledata17 = [roma_matrix.flatten()]
sampledata = np.append(sampledata, sampledata17, axis=0)

leicester_city_matrix = player_stats.loc[player_stats['team'] == 'leicester_city']
leicester_city_matrix = leicester_city_matrix[['Attacking Prowess:','Ball Control:','Dribbling:','Low Pass:','Lofted Pass:','Finishing:','Place Kicking:','Swerve:','Header:','Defensive Prowess:','Ball Winning:','Kicking Power:','Speed:','Explosive Power:','Unwavering Balance:','Physical Contact:','Jump:','Stamina:']].to_numpy()
sampledata18 = [leicester_city_matrix.flatten()]
sampledata = np.append(sampledata, sampledata18, axis=0)

sevilla_matrix = player_stats.loc[player_stats['team'] == 'sevilla']
sevilla_matrix = sevilla_matrix[['Attacking Prowess:','Ball Control:','Dribbling:','Low Pass:','Lofted Pass:','Finishing:','Place Kicking:','Swerve:','Header:','Defensive Prowess:','Ball Winning:','Kicking Power:','Speed:','Explosive Power:','Unwavering Balance:','Physical Contact:','Jump:','Stamina:']].to_numpy()
sampledata19 = [sevilla_matrix.flatten()]
sampledata = np.append(sampledata, sampledata19, axis=0)

lazio_matrix = player_stats.loc[player_stats['team'] == 'lazio']
lazio_matrix = lazio_matrix[['Attacking Prowess:','Ball Control:','Dribbling:','Low Pass:','Lofted Pass:','Finishing:','Place Kicking:','Swerve:','Header:','Defensive Prowess:','Ball Winning:','Kicking Power:','Speed:','Explosive Power:','Unwavering Balance:','Physical Contact:','Jump:','Stamina:']].to_numpy()
sampledata20 = [lazio_matrix.flatten()]
sampledata = np.append(sampledata, sampledata20, axis=0)

napoli_matrix = player_stats.loc[player_stats['team'] == 'napoli']
napoli_matrix = napoli_matrix[['Attacking Prowess:','Ball Control:','Dribbling:','Low Pass:','Lofted Pass:','Finishing:','Place Kicking:','Swerve:','Header:','Defensive Prowess:','Ball Winning:','Kicking Power:','Speed:','Explosive Power:','Unwavering Balance:','Physical Contact:','Jump:','Stamina:']].to_numpy()
sampledata21 = [napoli_matrix.flatten()]
sampledata = np.append(sampledata, sampledata21, axis=0)

getafe_matrix = player_stats.loc[player_stats['team'] == 'getafe']
getafe_matrix = getafe_matrix[['Attacking Prowess:','Ball Control:','Dribbling:','Low Pass:','Lofted Pass:','Finishing:','Place Kicking:','Swerve:','Header:','Defensive Prowess:','Ball Winning:','Kicking Power:','Speed:','Explosive Power:','Unwavering Balance:','Physical Contact:','Jump:','Stamina:']].to_numpy()
sampledata22 = [getafe_matrix.flatten()]
sampledata = np.append(sampledata, sampledata22, axis=0)

tottenham_matrix = player_stats.loc[player_stats['team'] == 'tottenham']
tottenham_matrix = tottenham_matrix[['Attacking Prowess:','Ball Control:','Dribbling:','Low Pass:','Lofted Pass:','Finishing:','Place Kicking:','Swerve:','Header:','Defensive Prowess:','Ball Winning:','Kicking Power:','Speed:','Explosive Power:','Unwavering Balance:','Physical Contact:','Jump:','Stamina:']].to_numpy()
sampledata23 = [tottenham_matrix.flatten()]
sampledata = np.append(sampledata, sampledata23, axis=0)

manchester_u_matrix = player_stats.loc[player_stats['team'] == 'manchester_united']
print(manchester_u_matrix)
manchester_u_matrix = manchester_u_matrix[['Attacking Prowess:','Ball Control:','Dribbling:','Low Pass:','Lofted Pass:','Finishing:','Place Kicking:','Swerve:','Header:','Defensive Prowess:','Ball Winning:','Kicking Power:','Speed:','Explosive Power:','Unwavering Balance:','Physical Contact:','Jump:','Stamina:']].to_numpy()
sampledata24 = [manchester_u_matrix.flatten()]
sampledata = np.append(sampledata, sampledata24, axis=0)

boca_juniors_matrix = player_stats.loc[player_stats['team'] == 'boca_juniors']
boca_juniors_matrix = boca_juniors_matrix[['Attacking Prowess:','Ball Control:','Dribbling:','Low Pass:','Lofted Pass:','Finishing:','Place Kicking:','Swerve:','Header:','Defensive Prowess:','Ball Winning:','Kicking Power:','Speed:','Explosive Power:','Unwavering Balance:','Physical Contact:','Jump:','Stamina:']].to_numpy()
sampledata25 = [boca_juniors_matrix.flatten()]
sampledata = np.append(sampledata, sampledata25, axis=0)

elo_array = np.array([[1984],[2118],[1872],[1945],[1978],[1930],[1913],[1867],[1838],[1830],[1812],[1809],[1795],[1794],[1793],[1792],[1791],[1785],[1774],[1773],[1766],[1756],[1756],[1745],[1739]])

X = sampledata
Y = elo_array
clf = tree.DecisionTreeRegressor()
clf = clf.fit(X, Y)

top10 = player_array[2100:2110]
print(top10)
top10_flat = [top10.flatten()]
print(top10_flat)

prediction = clf.predict(top10_flat)
print(prediction)


