# Mini-vidéos d'exemple (saynètes)

**Règle : dès que la voix donne un exemple, on le montre en mini-vidéo.** « À 200 ms, l'ennemi se téléporte » → on voit un perso tirer et l'ennemi se téléporter. « Sur 4 €, le streamer touche 2 € » → on voit la pièce partir du viewer, passer chez le streamer et en ressortir à moitié. Le spectateur doit pouvoir comprendre l'exemple **sans le son**.

Tu inventes la mini-vidéo à chaque fois, en assemblant des acteurs et des actions. Il n'y a pas de modèle tout fait : c'est à toi de raconter l'exemple en 2 à 4 secondes, qui tournent en boucle.

## Où la mettre
- **Scène `exemple`** (le cas principal) : 1 grande fenêtre, ou 2 fenêtres l'une sous l'autre pour comparer (avant/après, 20 ms/200 ms, wifi/câble).
  ```json
  {"type": "exemple", "texte": "Même tir, pas le même *ping*", "voix": "...",
   "fenetres": [
     {"titre": "20 ms", "couleur": "accent2", "saynete": {...}},
     {"titre": "200 ms", "couleur": "accent3", "saynete": {...}, "delai": 4.5}
   ]}
  ```
  La 2ᵉ fenêtre démarre par défaut à 42 % de la scène, pour suivre la voix qui parle d'abord du premier cas, puis du second. Avant de démarrer, elle reste figée et assombrie. Règle `delai` (en secondes depuis le début de la scène) si la voix arrive au 2ᵉ cas plus tôt ou plus tard.
- **Dans une autre scène** (`point`, `accroche`, `chiffre`, `fin`) : `"illustration": {"type": "saynete", "titre": "...", "saynete": {...}}`.

## Format d'une saynète
```json
{
  "duree": 3.2,            // durée d'une boucle (2,5 à 4,5 s)
  "boucle": true,          // rejoue en boucle (par défaut)
  "sol": 88,               // hauteur du sol en % (par défaut 88)
  "acteurs": {
    "toi":    {"forme": "perso", "couleur": "accent2", "x": 17, "taille": 48, "arme": true},
    "ennemi": {"forme": "perso", "couleur": "accent3", "x": 82, "taille": 48, "regard": "gauche"},
    "piece":  {"forme": "piece", "x": 30, "y": 50, "taille": 20, "visible": false}
  },
  "actions": [
    {"t": 0.8, "action": "tir", "de": "toi", "vers": "ennemi", "duree": 0.18}
  ]
}
```
(Les commentaires `//` servent juste à expliquer : ne les mets pas dans le vrai fichier.)

Coordonnées : `x` de 0 (gauche) à 100 (droite), `y` de 0 (haut) à 100 (bas). Pour un perso, `y` est la position des pieds (le sol par défaut). Pour une icône, c'est son centre. `taille` est en % de la hauteur de la fenêtre : 40 à 50 pour un perso, 18 à 35 pour un objet.

### Acteurs
| Champ | Valeurs |
|---|---|
| `forme` | `perso` (bonhomme bâton épais avec un casque gamer ; ses jambes bougent quand il se déplace), ou **n'importe quelle icône** de `illustrations.md` (`piece`, `serveur`, `pc`, `manette`, `live`, `coeur`, `trophee`...) |
| `couleur` | `accent` (jaune), `accent2` (cyan), `accent3` (rose), `rouge`, `vert`, `blanc`, `gris` ou `#RRGGBB` |
| `regard` | `droite` (par défaut) ou `gauche` (persos seulement) |
| `arme` | `true` : le perso tient un blaster (pour les tirs) |
| `expression` | `normal`, `content`, `surpris`, `fache`, `ko` |
| `visible` | `false` : l'acteur est caché au départ (il apparaît avec `apparait`) |

Mets toujours le perso du spectateur en **cyan (`accent2`)** et l'adversaire, ou l'autre personne, en **rose (`accent3`)** : c'est le même code couleur dans toutes les vidéos.

### Actions (toutes ont un `t`, l'instant en secondes dans la boucle)
| action | Champs | Effet |
|---|---|---|
| `deplace` | `qui`, `x` et/ou `y`, `duree` | Glisse en douceur vers la position |
| `teleporte` | `qui`, `x`, `y`, `glitch` (par défaut true) | Saut instantané avec un effet de bug (couleurs décalées, image découpée) et un fantôme qui reste à l'ancienne place : idéal pour le **lag** |
| `tir` | `de`, `vers` (un acteur) ou `x`/`y`, `duree`, `rate` (true = la balle continue jusqu'au bord), `couleur` | Flash au bout du canon + balle lumineuse avec traînée. La cible est l'endroit où se trouvait `vers` au moment du tir |
| `impact` | `sur` | Éclat + onde + l'acteur devient blanc une fraction de seconde et tremble |
| `tombe` | `qui` | Le perso tombe KO (yeux en X), allongé au sol |
| `expression` | `qui`, `expression` | Change la tête du perso |
| `regarde` | `qui`, `vers` (`droite`/`gauche`) | Le perso se retourne |
| `saute` | `qui`, `duree`, `hauteur` | Petit saut (joie, surprise) |
| `tremble` | `qui`, `duree` | Tremblement (peur, colère, choc) |
| `apparait` / `disparait` | `qui` | Apparition qui rebondit / disparition en fondu |
| `grandit` | `qui`, `echelle`, `duree` | Grossit (ex. un tas de pièces qui augmente) |
| `texte` | `texte`, `sur` (un acteur) ou `x`/`y`, `couleur`, `duree`, `taille` | Texte qui surgit puis monte doucement (« TOUCHÉ ! », « RATÉ », « +1 », « -50 % ») |
| `bulle` | `qui`, `texte`, `duree`, `taille` | Bulle de dialogue au-dessus du perso (« Hein ?! », « GG ») |
| `compteur` | `x`, `y`, `de`, `a`, `prefixe`, `suffixe`, `duree`, `couleur`, `taille` | Nombre qui défile (secondes d'attente, viewers, euros) |
| `lag` | `x`, `y`, `duree` | Petit rond de chargement qui tourne (écran figé) |
| `flash` | — | Flash blanc sur toute la fenêtre |

## Conseils de mise en scène
- **Une seule idée par fenêtre**, lisible en un coup d'œil : 2 ou 3 acteurs maximum.
- Laisse ~0,5 s de calme au début de la boucle, fais l'action, puis montre le **résultat** pendant au moins 1 s (« TOUCHÉ ! », une tête surprise). Le résultat, c'est ce que le spectateur retient.
- Pour comparer : **mêmes acteurs, mêmes positions, mêmes timings** dans les deux fenêtres. Seule la chose expliquée change. C'est ça qui rend la différence évidente.
- Ne mets rien dans le coin en haut à gauche (`x` < 25 et `y` < 25) : la pastille de titre de la fenêtre est là.
- Un `texte` au-dessus d'un perso : `y` entre 20 et 30. Deux textes dans la même fenêtre : écarte-les d'au moins 30 en `x`.
- Après le rendu, vérifie la mini-vidéo avec `--still` à 3 ou 4 instants de la boucle (début de scène + 0,5 s, + 1 s, + 1,5 s, + 2,5 s).

## Exemples qui marchent (copie-les et adapte-les)

**Le lag (ping 200 ms)** : voir la scène `exemple` de `exemples/ping.json`. Le joueur tire, l'ennemi se `teleporte` plus loin juste avant que la balle arrive, puis on affiche « RATÉ » et une bulle « Hein ?! ».

**Où va l'argent d'un sub** (1 fenêtre) :
```json
{"duree": 4.0, "acteurs": {
  "viewer": {"forme": "perso", "couleur": "accent2", "x": 14, "taille": 45},
  "piece": {"forme": "piece", "x": 24, "y": 55, "taille": 20, "visible": false},
  "streamer": {"forme": "perso", "couleur": "accent3", "x": 55, "taille": 45, "regard": "gauche"},
  "plateforme": {"forme": "serveur", "couleur": "accent", "x": 86, "y": 55, "taille": 34}},
 "actions": [
  {"t": 0.3, "action": "apparait", "qui": "piece"},
  {"t": 0.3, "action": "texte", "x": 24, "y": 28, "texte": "4 €", "duree": 1.2},
  {"t": 0.8, "action": "deplace", "qui": "piece", "x": 55, "y": 45, "duree": 0.6},
  {"t": 1.5, "action": "deplace", "qui": "piece", "x": 86, "y": 40, "duree": 0.5},
  {"t": 2.0, "action": "impact", "sur": "plateforme"},
  {"t": 2.0, "action": "disparait", "qui": "piece"},
  {"t": 2.1, "action": "texte", "x": 86, "y": 20, "texte": "-50 %", "couleur": "rouge", "duree": 1.6},
  {"t": 2.2, "action": "texte", "x": 50, "y": 20, "texte": "≈ 2 €", "couleur": "vert", "duree": 1.6},
  {"t": 2.3, "action": "expression", "qui": "streamer", "expression": "surpris"}]}
```

**Le délai d'un live** (le streamer répond 5 s après ton message) :
```json
{"duree": 4.0, "acteurs": {
  "streamer": {"forme": "perso", "couleur": "accent3", "x": 22, "taille": 45},
  "live": {"forme": "live", "x": 22, "y": 35, "taille": 16},
  "toi": {"forme": "perso", "couleur": "accent2", "x": 80, "taille": 45, "regard": "gauche"}},
 "actions": [
  {"t": 0.3, "action": "bulle", "qui": "toi", "texte": "Salut !", "duree": 1.0},
  {"t": 0.6, "action": "compteur", "x": 50, "y": 30, "de": 0, "a": 5, "suffixe": " s", "duree": 2.0},
  {"t": 1.5, "action": "expression", "qui": "toi", "expression": "fache"},
  {"t": 2.7, "action": "bulle", "qui": "streamer", "texte": "Salut toi !", "duree": 1.2},
  {"t": 2.7, "action": "saute", "qui": "streamer", "duree": 0.4},
  {"t": 2.8, "action": "expression", "qui": "toi", "expression": "content"}]}
```

**Autres idées faciles à monter** : wifi contre câble (2 fenêtres : une `manette` reliée à un `serveur`, et les paquets qui arrivent en retard avec `lag`) ; le smurf (un perso `gris` « Bronze » qui se fait éliminer d'un tir par un perso qui `grandit`) ; le raid (des persos qui `apparait` les uns après les autres, avec un `compteur` de viewers qui grimpe).
