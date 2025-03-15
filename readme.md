# Projet CAH (Classification Ascendante Hiérarchique)

## Description

Dans le cadre d'un cours de M1 "Algorithmique - Développement Python", j'ai fait ce projet dont l’objectif est de développer une série de classes Python permettant de mettre en œuvre l'algorithme de classification non supervisé CAH (classification ascendante hiérarchique).
Ce projet implémente une **Classification Ascendante Hiérarchique (CAH)** pour regrouper des textes en clusters selon leur similarité. Il récupère des textes depuis des pages web (scrap), les transforme en vecteurs et les classe. Le projet permet aussi d'ajouter ou supprimer des textes manuellement et d'afficher les résultats au format JSON.


## Fonctionnalités principales

- Tokenisation des textes
- Scraping de pages Wikisource
- Vecteur TF-IDF
- Calcul de similarité cosinus
- Classification ascendante hiérarchique (CAH)


## Structure des dossiers

- CAH.py : implémentation de la CAH
- tokenizer.py : tokenisation des textes
- ressources/ : fichiers stopwords.txt et grammar.txt pour le traitement des textes
- texts/ : dossier où les textes extraits des pages web seront enregistrés
- main.py : Point d'entrée du programme


## Dossiers ressources

- stopwords.txt : liste des mots à ignorer lors de la classification
- grammar.txt : fichier de grammaire pour la tokenisation


## Pistes d'amélioration

  - Gestion des caractères spéciaux dans l'affichage json
  - Récupération automatique de labels sur add_text et scrap_text
  - Affichage de la matrice de similarité
  - Utilisation d'un facteur tf_idf
  - Affichage d'une représentation en dendogramme
  - Incorporation des linkage_method single et complete à notre fonction classify
