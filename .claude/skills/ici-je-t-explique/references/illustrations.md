# Illustrations animées

Le but : **montrer ce que dit la voix**. Si la voix dit « aller-retour », on voit un aller-retour. Si elle dit « ça coûte cher », des pièces tombent. Une scène sans image paraît morte, alors donne une illustration à chaque scène (sauf `versus` et `liste`, qui ont leurs propres icônes).

## Comment l'ajouter
Dans une scène `accroche`, `texte`, `point`, `chiffre` ou `fin` :
```json
"illustration": "manette"                                   // une icône seule, animée
"illustration": "chrono"                                    // une animation sans réglage
"illustration": {"type": "aller_retour", "gauche": "pc", "droite": "serveur", "label_gauche": "Ton PC"}
```
- Scène `versus` : `"gauche_icone": "wifi", "droite_icone": "cable"` (une icône dans chaque carte).
- Scène `liste` : `"icones": ["cable", "globe", "telechargement"]` (une icône par élément, à la place du numéro).

Quand une scène a une illustration, le texte descend automatiquement sous l'image et passe à 2-3 lignes au maximum. Garde donc un `texte` court.

## Les animations

| type | Ce qu'on voit | Options | Idéal pour |
|---|---|---|---|
| `aller_retour` | Deux icônes ; une flèche cyan part, une rose revient, et une boule lumineuse fait l'aller-retour en boucle | `gauche`, `droite` (noms d'icônes), `label_gauche`, `label_droite`, `centre` (texte au milieu, ex. « 20 ms »), `periode` | Ping, requête/réponse, question/réponse, échange |
| `transfert` | Deux icônes ; un flux de points lumineux va de l'une à l'autre | `gauche`, `droite`, `sens` (`droite`/`gauche`), `label_gauche`, `label_droite`, `centre` | Téléchargement, upload, stream envoyé aux viewers, argent qui passe d'un compte à l'autre |
| `chrono` | Chronomètre dont l'aiguille tourne et remplit un arc | `tours_par_seconde`, `texte` | Temps, délai, latence, durée |
| `graphique` | Barres qui montent une à une, puis une flèche de tendance | `valeurs` (entre 0 et 1), `sens` (`hausse`/`baisse`), `etiquettes` | Croissance, évolution, stats, comparaison chiffrée |
| `pieces` | Des pièces qui tombent en tournant et s'empilent | `nombre`, `nom` (icône, `piece` par défaut, ou `billet`) | Argent, prix, revenus, subs, dons |
| `chat` | Un chat de live qui défile, avec des cœurs qui montent | `messages` (liste de textes courts), `rythme` | Twitch, communauté, commentaires, raid, fin de vidéo |
| `cible` | Un viseur qui cherche puis touche, avec un hitmarker et un éclat | `cible` (icône visée, `personne` par défaut) | FPS, hitbox, visée, précision, « headshot » |
| `wifi` | Des ondes wifi qui s'allument | `force` (0 à 3 ; en dessous de 3, un « ! » rouge clignote) | Connexion, réseau, mauvaise connexion |
| `chargement` | Une barre de progression rayée avec un pourcentage | `jusqua` (0 à 1), `duree`, `texte` | Chargement, téléchargement, progression, XP |
| `alerte` | Un panneau qui tremble avec des ondes d'alerte | `nom` (icône, `alerte` par défaut) | Danger, arnaque, piège, erreur courante |
| `icone` | Une icône qui apparaît en rebondissant, avec un halo, un éclat et des étincelles | `nom`, `taille`, `couleur` (`accent`, `accent2`, `accent3`) | N'importe quel objet du catalogue ci-dessous |
| `icones` | 2 à 4 icônes en ligne, avec ou sans flèches entre elles | `noms`, `liens` (`fleche`/`plus`), `labels` | Une chaîne (PC → box → serveur), une recette (A + B), du matériel |
| `fleche` | Une grosse flèche qui jaillit, avec des traits de vitesse | `sens` (`haut`/`bas`/`gauche`/`droite`), `couleur` | Hausse, baisse, « ça monte », direction |

## Les icônes (pour `icone`, `icones`, `gauche`/`droite`, `*_icone`, `icones`)
`pc` `ecran` `serveur` `manette` `console` `telephone` `clavier` `souris` `casque` `micro` `camera` `gpu` `wifi` `cable` `globe` `telechargement` `live` `bulle` `coeur` `personne` `piece` `billet` `trophee` `etoile` `eclair` `fusee` `alerte` `check` `croix` `oeil` `cadenas` `cible` `chrono` `horloge` `cerveau`

Il n'y a volontairement **aucun logo de marque** (Twitch, Discord, PlayStation…) ni personnage de jeu : pour parler de Twitch, utilise `live` + `chat` ; pour une console, `console` ou `manette`.

## Correspondances rapides
- Twitch, stream, live → `chat`, `icone live`, `icone camera`, `icone micro`
- Abonnés, viewers → `icones` avec des `personne`, `graphique`
- Argent, prix, salaire → `pieces`, `icone billet`
- Rapidité, performance → `icone eclair`, `fleche haut`, `icone fusee`
- Vrai ou faux → `icone check` / `icone croix` (ou en `versus` : `gauche_icone: check`, `droite_icone: croix`)
- Cerveau, tilt, réflexes → `icone cerveau`, `chrono`
- Sécurité, compte piraté → `alerte`, `icone cadenas`
- Matériel PC → `icones` avec `gpu`, `clavier`, `souris`
- Classement, victoire → `icone trophee`, `graphique`
