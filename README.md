# Project Title

Jouer au Morpion grâce au Monte Carlo tree search

## Description
Ce projet académique s'inspire d' un code trouvé sur <a href = 'https://gist.github.com/eaorak/3966315'>ce repo github</a> pour créer un objet qui permet de jouer au morpion de manière interactive contre un "adversaire" à la politique très simple : 

- Si l'ordinateur peut gagner au coup suivant, il le joue
- Si le joueur peut gagner au coup suivant, il le contre
- Sinon il joue un coup de manière aléatoire (Différence par rapport au code initial où l'ordinateur jouait alors de manière déterministe en fonction des cases libres sur le plateau)

Nous avons amélioré ce code pour pouvoir également simuler des parties de jeu où le joueur joue automatiquement contre l'ordinateur à partir d'une politique précise .

- Soit il s'agit de la même politique que l'ordinateur décrite plus haut.
- Soit il s'agit d'une politique déterminée par l'algorithme Monte Carlo Tree search. 

Lancer le notebook Tic_Tac_toe pour la démo.



### Librairies

- pandas
- numpy 
- mctspy. Package disponible sur <a href='https://github.com/int8/monte-carlo-tree-search'> Ce repo github </a>. Vous pouvez l'installer avec un pip install mctspy





## Authors

* **Clotilde Miura et Manon Rivoire** 

