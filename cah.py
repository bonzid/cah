import json
from tokenizer import Tokeniseur
from lxml import html
import requests
import os

stop_path="ressources/stopwords.txt"
tokenizer_instance = Tokeniseur()

class CAH:
  """
  On construit une classe CAH avec les propriétés suivantes :
    - propriété 1 : data de structure JSON
    - propriété 2 : linkage_method "average", "min", "max"

  Ainsi que les méthodes suivantes :
    - méthode 1 : add_text(label:str,text:str) pour ajouter un texte à nos données
    - méthode 2 : del_text(label:str) pour supprimer un texte selon le label
    - méthode 3 : classify(n:int,min_sim:float)->list, qui renvoie au résultat de la classification ascendante s'arrêtant à n classes ou à une similarité minimale
    - méthode 4 privée : _dissim(cluster1:list,cluster2:list)->float
    - méthode 5 statique : sim_cosinus(vect1:dict,vect2:dict)->float
    - méthode 6 statique : text2vec(text:str,stoplist:set)->dict
    - méthode 7 statique : read_stoplist(filename:str)->set
  """

  def __init__(self,data,linkage_method,stop_path="/ressources/stopwords.txt"):
    self.data={}
    self.linkage_method=linkage_method
    self.tokenizer=Tokeniseur
    self.stop_path=stop_path


  def afficher_data_json(self):
    """
    Affiche les données au format JSON
    Nécessite les modules suivants : json
    """
    data_json=json.dumps(self.data,indent=2)
    print(data_json)


  @staticmethod
  def read_stoplist(stop_path:str)->set:
    """
    Cette fonction lit un fichier de stopwords et renvoie à un ensemble de mots

    Entrée :
      arg: chemin vers le fichier
    Sortie :
      set: ensemble de mots à ignorer lors du traitement
    """
    #On initie ici le set "stoplist" pour pouvoir y stocker le contenu des lignes de notre fichier
    stoplist=set()

    try:
      with open(stop_path,'r',encoding='utf-8') as file:
        #Pour chaque ligne du fichier, on ajoute son contenu à notre set stoplist
        for line in file.readlines():
          stoplist.add(line.strip())

    except FileNotFoundError:
      print(f"Fichier de stoplist introuvable à l'adresse {stop_path}.\n")

    return stoplist


  def add_text(self,label:str,text:str):
    """
    Cette fonction ajoute un texte à nos données à partir d'un texte donné par l'utilisateur.

    Entrées :
      arg1 : le label du texte à ajouter
      arg2 : le texte à ajouter
    """

    if label not in self.data:
      #On appelle Tokeniseur depuis l'instance tokenizer
      #print(text)
      tokens=tokenizer_instance.tokenize(text)
      stoplist=self.read_stoplist(self.stop_path)
      vector=self.text2vec(text,stoplist)

      self.data[label]={"label":label,"vecteur":vector,"tf_idf":None}
      add_process=print(f"-------------Le texte {label} a bien été ajouté aux données.-------------\n")

    elif label in self.data:
      add_process=print(f"Le label {label} est déjà utilisé.\n")

    else:
      add_process=print(f"Le texte {label} n'a pas pu être ajouté aux données.\n")

    return add_process


  def del_text(self,label:str):
    """
    Cette fonction supprime le texte de nos données selon un label donné.

    Entrée :
      - le label du texte à supprimer
    """
    #On vérifie si label existe dans data
    if label in self.data:
      #Si oui, on le supprime avec del
      del self.data[label]
      del_process=print(f"Le texte {label} a bien été supprimé.\n")

    #Sinon, on affiche label introuvable
    else:
      del_process=print(f"Le label {label} est introuvable.\n")

    return del_process


  @staticmethod
  def text2vec(text:str,stoplist:set)->dict:
    """
    Cette fonction convertit du texte brut en un vecteur de nombres
    Entrées :
      arg1 : le texte à convertir
      arg2: notre stoplist
    Sortie :
      un dictionnaire associant un token à sa fréquence absolue dans le texte
    """

    tokens=tokenizer_instance.tokenize(text)
    stoplist=CAH.read_stoplist(stop_path)

    #On initie notre dictionnaire vector vide
    vector={}
    for token in tokens:
      #Si le token est dans notre stoplist, on l'ignore
      if token not in stoplist:
        #Si le token n'est pas dans notre dictionnaire, on l'ajoute
        if token not in vector:
          vector[token]=0
        #Si il est déjà dans le dictionnaire, on ajoute 1 à sa fréquence
        vector[token]+=1

    return vector


  def scrap_text(self,label:str,url:str)->str:
    """
    Cette fonction ajoute un texte à nos données en récupérant le contenu des balises <p> d'une page Web.

    Entrées :
      arg1 : le label du texte à ajouter
      arg2 : l'url de la page Web
    Sortie :
      la chaîne de caractères du contenu des balises

    Nécessite les modules suivants : lxml, html, requests
    """
    page=requests.get(url)

    if page.status_code==200:
      tree=html.fromstring(page.content)

      #On pioche ici notre contenu dans les balises p
      divs=tree.xpath('//p')

      #On récupère le texte qu'il y a dans chaque balise p
      content=[]
      for div in divs:
        content.append(div.text_content())

      #On crée notre chaîne de caractères à partir des éléments de la liste content
      page_content=" ".join(content)

      #On écrit ce contenu dans un nouveau fichier avec le label donné
      file_path=os.path.join('texts', f'{label}.txt')
      with open(file_path,'w',encoding='utf-8') as file:
        for text in content:
          file.write(text+'\n')

      print(f"Le contenu de la page a été enregistré dans le fichier {label}.txt.\n")
    else:
      print("Le contenu de la page n'a pas pu être enregistré.\n")


    #Pour ajouter le texte à nos données
    self.add_text(label,page_content)
    #print(f"-------------Le texte {label} a bien été ajouté aux données.-------------\n")

    return page_content


  def sim_cosinus(self,vect1:dict,vect2:dict)->float:
    """
    Cette fonction calcule la similarité cosinus entre deux vecteurs

    Entrées :
    arg1 : premier vecteur sous forme de dictionnaire (chaque mot d'un texte associé à sa fréquence absolue)
    arg2 : deuxième vecteur sous forme de dictionnaire

    Sortie :
    un float valeur de similarité cosinus entre les deux vecteurs donnés
    """

    #On fait un set (liste) des clés uniques de chaque vecteur
    keys=set(vect1.keys()).union(set(vect2.keys()))

    #On calcule ici la somme des produits scalaires
    scalaire=sum(vect1.get(key,0)*vect2.get(key,0) for key in keys)
    norm1=sum(value**2 for value in vect1.values())**0.5
    norm2=sum(value**2 for value in vect2.values())**0.5

    #Dans le cas où l'une des deux normes est =0
    if norm1==0 or norm2==0:
      return 0.0

    #On calcule la similarité grâce au produit scalaire et aux normes
    similarite=scalaire/(norm1*norm2)
    return similarite



  def _dissim(self,cluster1:list,cluster2:list)->float:
    """
    Calcule la dissimilarité entre deux clusters.

    Entrées :
    - cluster1: liste des labels du premier cluster
    - cluster2: liste des labels du deuxième cluster

    Sortie :
    La dissimilarité moyenne entre les paires de textes des deux clusters
    """
    #Ici on initie la somme des dissimilarités et le compteur de paires
    dissimilarite_sum=0
    paires=0

    #pour chaque texte dans chaque cluster, on parcourt le nb de paires entre les deux clusters
    for text1 in cluster1:
      for text2 in cluster2:
        #On récupère les vecteurs associés aux textes
        vect1=self.data[text1]["vecteur"]
        vect2=self.data[text2]["vecteur"]

        #On calcule la somme de dissim avec sim_cosinus
        dissimilarite_sum+=1-self.sim_cosinus(vect1, vect2)

        #On incrémente le nb de paires
        paires+=1

    #Si aucune paire présente, _dissim=0
    if paires==0:
      return 0.0

    #On fait un return sur la dissimilarité moyenne
    average_dissimilarite=dissimilarite_sum/paires
    return average_dissimilarite


  def classify(self,n:int=None,min_sim:float=None)->list:
    """
    Cette fonction renvoie le résultat de la classification ascendante hiérarchique en s'arrêtant à n classes ou à une similarité minimale.
    Si les deux valeurs sont donnés par l'utilisateur, seulement n sera pris en compte.

    Entrée :
    -n: le nombre de clusters souhaité
    -min_sim: la similarité minimale entre les textes au sein d'un cluster pour arrêter la classification

    Sortie :
    Une liste de listes de labels
    """
    #On vérifie si l'utilisateur a donné n, min_sim ou les deux
    #cas où n et min_sim sont donnés: on ignore min_sim
    if n is not None and min_sim is not None:
      min_sim=None

    #cas où seulement min_sim a été donné, on introduit un n=1
    if n is None and min_sim is not None:
      n=1

    #On initie un cluster (liste) avec pour chaque cluster un texte de notre data
    clusters=[[label] for label in self.data.keys()]

    #Tant que le nombre de clusters est supérieur à n, alors:
    while len(clusters)>n:

      #on initie merge_indices qui nous servira à suivre les clusters qui seront fusionnés ds clusters
      merge_indices=None

      #initier min_sim comme un "grand" float qui sera actualisé plus tard
      min_dissim=1000.0

    #On calcule la dissimilarité entre tous les paires de clusters
    #on exclut le dernir cluster de notre boucle pour éviter de comparer le dernier cluster avec lui-meme
      for i in range(len(clusters)-1):
        #on prend le cluster après le cluster i
        for j in range(i+1,len(clusters)):
          #on calcule la dissimilarité entre les deux clusters en faisant appel à dissim
          dissimilarite=self._dissim(clusters[i],clusters[j])

          #On ne retient à chaque fois que le minimum de dissim donc:
          ##Ici on pourrait ajouter differentes affectations selon si linkage_method=="average","single" ou "complete"?
          if dissimilarite<min_dissim:
            #maj de min_dissim si résultat de _dissim plus petit que min_dissim
            min_dissim=dissimilarite

            #merge_indices prend les valeurs de i et j, indices des clusters traités
            merge_indices=(i,j)

      if merge_indices is None:
        break

      #On fusionne les clusters (listes) qui ont une dissim minimale
      merged_cluster=clusters[merge_indices[0]]+clusters[merge_indices[1]]

      #Ici on supprime le deuxième cluster fusionné selon l'indice merge_indices
      clusters.pop(merge_indices[1])
      #Ici on remplace le premier cluster avec notre nouveau cluster fusionné
      clusters[merge_indices[0]]=merged_cluster

      #On calcule la similarité moyenne entre les textes du nouveau cluster
      sim=sum(self._dissim([text],merged_cluster) for text in merged_cluster)/len(merged_cluster)
      #print(sim)

      #Si la similarité moyenne est inférieure à min_sim donnée, on arrête la boucle
      if min_sim is not None and sim<min_sim:
        break


    for i,cluster in enumerate(clusters,start=1):
      print(f"\n-------------Cluster {i} formé-------------")
      print(f"{cluster}\n")

    return clusters
