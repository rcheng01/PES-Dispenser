import pickle
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import re
import time
from sklearn.tree import DecisionTreeRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.svm import SVR
from itertools import permutations
from itertools import islice
from matplotlib import pyplot as plt
from IPython.display import display, HTML

player_stats = pd.read_csv("player_stats.csv")
player_stats.to_excel("output.xlsx")

teams = {
    "liverpool": ['S. MANÉ', 'ROBERTO FIRMINO', 'M. SALAH', 'N. KEÏTA', 'G. WIJNALDUM', 'J. HENDERSON', 'A. ROBERTSON',
                  'V. VAN DIJK', 'D. LOVREN', 'T. A. ARNOLD'],
    "barcelona": ['A. GRIEZMANN', 'L. SUÁREZ', 'L. MESSI', 'F. DE JONG', 'I. RAKITIĆ', 'SERGI ROBERTO', 'JORDI ALBA',
                  'C. LENGLET', 'PIQUÉ', 'NÉLSON SEMEDO'],
    "manchester_city": ['R. STERLING', 'S. AGÜERO', 'L. SANÉ', 'BERNARDO SILVA', 'FERNANDINHO', 'İ. GÜNDOĞAN',
                        'B. MENDY', 'V. KOMPANY', 'J. STONES', 'K. WALKER'],
    "bayern_munchen": ['J. RODRÍGUEZ', 'R. LEWANDOWSKI', 'THIAGO A.', 'P. COUTINHO', 'T. MÜLLER', 'L. GORETZKA',
                       'D. ALABA', 'M. HUMMELS', 'J. BOATENG', 'J. KIMMICH'],
    "juventus": ['DOUGLAS COSTA', 'C. RONALDO', 'P. DYBALA', 'B. MATUIDI', 'M. PJANIĆ', 'S. KHEDIRA', 'L. SPINAZZOLA',
                 'G. CHIELLINI', 'L. BONUCCI', 'JOÃO CANCELO'],
    "ajax": ['D. TADIĆ', 'Q. PROMES', 'D. VAN DE BEEK', 'H. ZIYECH', 'DAVID NERES', 'É. ÁLVAREZ', 'N. TAGLIAFICO',
             'D. BLIND', 'J. VELTMAN', 'N. MAZRAOUI'],
    "psg": ["NEYMAR", "E. CAVANI", "K. MBAPPÉ", "M. VERRATTI", "L. PAREDES", "A. RABIOT", "L. KURZAWA", "THIAGO SILVA",
            "MARQUINHOS", "DANI ALVES"],
    "real_madrid": ["VINÍCIUS JÚNIOR", "K. BENZEMA", "G. BALE", "L. MODRIĆ", "CASEMIRO", "ISCO", "MARCELO",
                    "SERGIO RAMOS", "R. VARANE", "DANIEL CARVAJAL"],
    "flamengo:": ["M. MORENO", "F. URIBE", "GEUVÂNIO", "R. PIRIS", "WILLIAN ARÃO", "DIEGO", "RENÊ", "LÉO DUARTE",
                  "RHODOLFO", "RODINEI"],
    "atletico_madrid": ["N. KALINIĆ", "DIEGO COSTA", "VITOLO", "SAÚL", "T. PARTEY", "KOKE", "FILIPE LUIS", "D. GODÍN",
                        "L. HERNANDEZ", "S. ARIAS"],
    "inter_milan": ["H. ÇALHANOĞLU", "K. PIĄTEK", "SUSO", "G. BONAVENTURA", "L. BIGLIA", "LUCAS PAQUETÁ",
                    "R. RODRÍGUEZ", "A. ROMAGNOLI", "M. CALDARA", "D. CALABRIA"],
    "benfica": ["F. CERVI", "H. SEFEROVIĆ", "E. SALVIO", "PIZZI", "L. FEJSA", "GABRIEL PIRES", "ÁLEX GRIMALDO",
                "RÚBEN DIAS", "G. CONTI", "ANDRÉ ALMEIDA"],
    "fc_porto": ["V. ABOUBAKAR", "J. CORONA", "TIQUINHO SOARES", "H. HERRERA", "DANILO PEREIRA", "Y. BRAHIMI",
                 "ALEX TELLES", "FELIPE", "PEPE", "M. PEREIRA"],
    "chelsea": ["E. HAZARD", "G. HIGUAÍN", "WILLIAN", "N. KANTÉ", "JORGINHO", "R. BARKLEY", "MARCOS ALONSO",
                "A. RÜDIGER", "DAVID LUIZ", "AZPILICUETA"],
    "atalanta": ["D. ZAPATA", "R. GOSENS", "H. HATEBOER", "M. DE ROON", "R. FREULER", "J. ILIČIĆ", "RAFAEL TOLÓI",
                 "A. MASIELLO", "J. PALOMINO", "G. MANCINI"],
    "valencia": ["SANTI MINA", "GONÇALO GUEDES", "RODRIGO", "D. CHERYSHEV", "G. KONDOGBIA", "DANI PAREJO", "JOSÉ GAYÁ",
                 "E. GARAY", "GABRIEL", "C. PICCINI"],
    "shakhtar_donetsk": ["O. KAYODE", "JÚNIOR MORAES", "MARLOS", "MAYCON", "T. STEPANENKO", "TAISON", "ISMAILY",
                         "I. ORDETS", "S. KRIVTSOV", "B. BUTKO"],
    "roma": ["D. PEROTTI", "E. DŽEKO", "C. ÜNDER", "L. PELLEGRINI", "D. DE ROSSI", "J. PASTORE", "A. KOLAROV",
             "K. MANOLAS", "F. FAZIO", "A. FLORENZI"],
    "leicester_city": ["M. ALBRIGHTON", "J. VARDY", "K. IHEANACHO", "Y. TIELEMANS", "W. NDIDI", "J. MADDISON",
                       "B. CHILWELL", "H. MAGUIRE", "J. EVANS", "RICARDO PEREIRA"],
    "sevilla": ["L. OCAMPOS", "L. DE JONG", "RONY LOPES", "N. GUDELJ", "FERNANDO", "É. BANEGA", "ESCUDERO",
                "DIEGO CARLOS", "DANIEL CARRIÇO", "SERGI GÓMEZ"],
    "lazio": ["M. PAROLO", "C. IMMOBILE", "F. CAICEDO", "S. M. SAVIĆ", "LUCAS LEIVA", "LUIS ALBERTO", "J. LUKAKU",
              "F. ACERBI", "WALLACE", "D. BASTA"],
    "napoli": ["L. INSIGNE", "D. MERTENS", "JOSÉ CALLEJÓN", "ALLAN", "P. ZIELIŃSKI", "FABIÁN RUIZ", "F. GHOULAM",
               "K. KOULIBALY", "ALBIOL", "K. MALCUIT"],
    "getafe": ["JAIME MATA", "ÁNGEL", "G. SHIBASAKI", "N. MAKSIMOVIĆ", "BERGARA", "BERGARA", "V. ANTUNES", "D. DAKONAM",
               "BRUNO", "D. SUÁREZ"],
    "tottenham": ["SON HEUNG-MIN", "H. KANE", "LUCAS MOURA", "D. ALLI", "E. DIER", "C. ERIKSEN", "D. ROSE",
                  "T. ALDERWEIRELD", "J. VERTONGHEN", "K. TRIPPIER"],
    "manchester_united": ["A. SÁNCHEZ", "R. LUKAKU", "J. LINGARD", "P. POGBA", "N. MATIĆ", "FRED", "L. SHAW",
                          "E. BAILLY", "P. JONES", "A. VALENCIA"],
    "boca_juniors": ["R. ÁBILA", "D. BENEDETTO", "C. PAVÓN", "N. NÁNDEZ", "I. MARCONE", "E. REYNOSO", "F. FABRA",
                     "C. IZQUIERDOZ", "P. GOLTZ", "J. BUFFARINI"],
    "bad_team": ["P. AUBAMEYANG","A. LACAZETTE","D. WELBECK","A. IWOBI","H. MKHITARYAN","A. RAMSEY","DENIS SUÁREZ","M. ÖZIL","L. TORREIRA","NACHO MONREAL"],
    "badteam2": ["R. ASSALÉ","J. NSAMÉ","G. HOARAU","K. MBABU","C. FASSNACHT","M. SULEJMANI","D. SOW","DIEGO SOUZA","S. TRÉLLEZ","L. BENITO"]}


def get_team(playername):
    for team in teams:
        if playername in teams[team]:
            return team


player_stats['team'] = player_stats['Name:'].apply(lambda x: get_team(x))
numbers_stats = player_stats[
    ['Attacking Prowess:', 'Ball Control:', 'Dribbling:', 'Low Pass:', 'Lofted Pass:', 'Finishing:', 'Place Kicking:',
     'Swerve:', 'Header:', 'Defensive Prowess:', 'Ball Winning:', 'Kicking Power:', 'Speed:', 'Explosive Power:',
     'Unwavering Balance:', 'Physical Contact:', 'Jump:', 'Stamina:']]

player_array = numbers_stats.to_numpy()

list_of_teams = []
for team in teams:
    if team != 'roma':
        sample_matrix = player_stats.loc[player_stats['team'] == team]
        sample_matrix = sample_matrix[
            ['Attacking Prowess:', 'Ball Control:', 'Dribbling:', 'Low Pass:', 'Lofted Pass:', 'Finishing:',
             'Place Kicking:', 'Swerve:', 'Header:', 'Defensive Prowess:', 'Ball Winning:', 'Kicking Power:', 'Speed:',
             'Explosive Power:', 'Unwavering Balance:', 'Physical Contact:', 'Jump:', 'Stamina:']]
        for i in range(100):
            samplematrix_shuffled = sample_matrix.sample(frac=1)
            list_of_teams.append(samplematrix_shuffled)

list_of_teams = [team.to_numpy().flatten() for team in list_of_teams]
sample_data = np.stack(list_of_teams)

elo_array = [[1984], [2118], [1872], [1945], [1978], [1930], [1913], [1867], [1838], [1830], [1812], [1809], [1795],
             [1794], [1793], [1792], [1791], [1785], [1774], [1773], [1766], [1756], [1756], [1745], [1739],[1737],[1717]]

big_elo = []
for elo in elo_array:
    for i in range(100):
        big_elo.append(elo)

big_elo = np.array(big_elo)

roma_matrix = player_stats.loc[player_stats['team'] == 'roma']
roma_matrix = roma_matrix[
    ['Attacking Prowess:', 'Ball Control:', 'Dribbling:', 'Low Pass:', 'Lofted Pass:', 'Finishing:', 'Place Kicking:',
     'Swerve:', 'Header:', 'Defensive Prowess:', 'Ball Winning:', 'Kicking Power:', 'Speed:', 'Explosive Power:',
     'Unwavering Balance:', 'Physical Contact:', 'Jump:', 'Stamina:']].to_numpy()
roma_data = [roma_matrix.flatten()]

X = sample_data
Y = big_elo
clf = DecisionTreeRegressor(random_state = 0)
clf.fit(X,Y)
# clf = MLPRegressor()
# clf = clf.fit(X, Y)
# clf = SVR(C=1.0, epsilon=0.2)
# clf.fit(X, Y)

# prediction = clf.predict(top10_flat)
# print(prediction)


player_stats["unique_name"] = player_stats["Name:"] + player_stats.index.map(str)

top1000 = player_stats.loc[0:1000, :]

current_team_names = player_stats.loc[990:999, "unique_name"].tolist()
new_player_names = player_stats.loc[0:990, "unique_name"].tolist()
all_player_names = player_stats.loc[0:1000, "unique_name"].tolist()

def test_player(new_player_name, slot_to_replace):
    old_player_names = current_team_names.copy()
    if new_player_name in old_player_names and new_player_name != old_player_names[slot_to_replace]:
        return -1
    old_player_names[slot_to_replace] = new_player_name
    old_player_data = player_stats[player_stats["unique_name"].isin(old_player_names)]
    old_player_data = old_player_data[
        ['Attacking Prowess:', 'Ball Control:', 'Dribbling:', 'Low Pass:', 'Lofted Pass:', 'Finishing:',
         'Place Kicking:', 'Swerve:', 'Header:', 'Defensive Prowess:', 'Ball Winning:', 'Kicking Power:', 'Speed:',
         'Explosive Power:', 'Unwavering Balance:', 'Physical Contact:', 'Jump:', 'Stamina:']]
    old_player_seed = [old_player_data.to_numpy().flatten()]
    new_elo = clf.predict(old_player_seed)
    if not isinstance(new_elo,float):
        return new_elo[0]
        raise ValueError("new elo is of type", type(new_elo))
    return new_elo

# elos = []
# for i in range(3):
#     for slot in range(10):
#         top1000["test_elo"] = top1000["unique_name"].apply(lambda name: test_player(name, slot))
#         best_player_index = top1000["test_elo"].idxmax()
#         elos.append(top1000["test_elo"].max())
#         best_player = player_stats.loc[best_player_index, "unique_name"]
#         current_team_names[slot] = best_player
#
# print(current_team_names)
# print(elos)
#
# XVALUES = list(range(30))
# YVALUES = elos
# plt.plot(XVALUES, YVALUES)
# plt.xlabel("number of player swaps")
# plt.ylabel("elo")
# plt.title("Algorithmic Improvement of Team via Hill Climbing")
# plt.show()
