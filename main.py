from cah import CAH 
from tokenizer import Tokeniseur 
import json
from lxml import html
import requests

def main():
    stop_path="ressources/stopwords.txt"
    grm_path="ressources/grammar.txt"
    
    tokenizer=Tokeniseur(grm_path)
    Tokeniseur.read_grammar(grm_path)

    #On crée une instance pour notre classe CAH
    cah_instance=CAH(data={},linkage_method="average",stop_path=stop_path)

    #On ajoute des textes à partir de différentes URL
    cah_instance.scrap_text("1_Esprit","https://fr.wikisource.org/wiki/L%E2%80%99Esprit_de_corps")
    cah_instance.scrap_text("2_Serin","https://fr.wikisource.org/wiki/Le_Serin_et_le_Moineau")
    cah_instance.scrap_text("3_Cheval","https://fr.wikisource.org/wiki/Le_Cheval_et_l%E2%80%99%C3%A2ne_(Gleim)")
    cah_instance.scrap_text("4_Serin","https://fr.wikisource.org/wiki/Le_Serin_et_le_Moineau")
    cah_instance.scrap_text("5_Impunite","https://fr.wikisource.org/wiki/L%E2%80%99Impunit%C3%A9_de_groupe")
    cah_instance.scrap_text("6_Sociologie","https://fr.wikisource.org/wiki/La_Sociologie_politique")

    #On ajoute un texte donné par l'utilisateur directement avec add_text
    cah_instance.add_text("7_Citoyens","Beaucoup de personnes de considération, parmi les citoyens de la ville, contribuèrent, par leurs libéralités et leurs charités, à l’accroissement et à l’embellissement du Grand Hôtel-Dieu. Sa situation d’alors était celle qu’il a aujourd’hui, le long du quai de Retz, sur les anciennes courtines du Rhône, et depuis la chapelle du Saint-Esprit, jusqu’à la boucherie de l’hôpital. L’administration, confiée d’abord à des laïques, passa, en 1172, aux religieux de Haute-Combe, en Savoie, puis aux Bernardins de la Chassagne, en Bresse, et en 1486, elle revint au Consulat, et finalement, en 1583, rendue aux citoyens. Les administrateurs furent choisis dans les différents ordres de la ville.")

    #On peut ici afficher nos données au format JSON avant la classification
    cah_instance.afficher_data_json()

    #Test de del_text sur nos données
    cah_instance.del_text("1_Esprit")
    cah_instance.afficher_data_json()

    #Test de classify sur nos données
    #Les textes 2_Serin et 4_Serin sont identiques et devraient se retrouver dans le même cluster.
    resultat_classification=cah_instance.classify(4)

if __name__=="__main__":
    main()
