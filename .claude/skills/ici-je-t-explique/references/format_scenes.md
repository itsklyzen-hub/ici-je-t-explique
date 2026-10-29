# Format de `scenes.json`

(Les commentaires `//` servent juste à expliquer : ne les mets pas dans le vrai fichier.)

```jsonc
{
  "serie": "Ici je t'explique",        // pastille en haut (optionnel)
  "titre": "C'est quoi le *ping* ?",    // titre fixe en haut (optionnel, *mot* = jaune)
  "sous_titres": true,                  // false pour les désactiver
  "couleurs": {"accent": "#FFD60A"},    // optionnel : fond1, fond2, grille, texte, accent, accent2, accent3
  "scenes": [ ... ]
}
```

Chaque scène peut avoir une `illustration` (animation ou icône) : voir `illustrations.md`. Pour `versus`, utilise `gauche_icone` et `droite_icone` ; pour `liste`, utilise `icones`.

Chaque scène a un `type`, une `voix` (le texte lu, qui sert au calage et aux sous-titres) et ses champs propres. `debut` et `fin` (en secondes) sont optionnels : si **toutes** les scènes en ont, ils sont utilisés tels quels. Sinon, le calage est automatique sur la voix.

Dans tous les textes affichés, `*un ou plusieurs mots*` passe en couleur d'accent. Un « ? » ou un « ! » isolé reste collé au mot d'avant.

| type | Champs | Rendu |
|---|---|---|
| `accroche` | `texte` (≤ 10 mots) | Gros texte, mots qui apparaissent un par un avec un petit tremblement |
| `point` | `numero` (optionnel), `texte`, `detail` (optionnel, 1 ligne) | Pastille rose numérotée + idée + précision en plus petit |
| `chiffre` | `valeur` (nombre), `unite` (optionnel), `decimales` (optionnel), `texte` | Compteur qui monte jusqu'à la valeur + phrase dessous |
| `versus` | `gauche`, `gauche_detail`, `droite`, `droite_detail`, `gauche_icone`, `droite_icone`, `texte` (optionnel) | Deux cartes (cyan en haut, rose en bas) avec « VS » + conclusion |
| `exemple` | `fenetres` (1 ou 2 : `titre`, `couleur`, `saynete`, `delai`), `texte` (court) | Mini-vidéo(s) d'exemple dans des fenêtres façon écran de jeu (voir `saynetes.md`) |
| `liste` | `texte` (titre), `items` (2 à 5, ≤ 30 caractères chacun), `icones` (optionnel, une par élément) | Éléments numérotés qui apparaissent un par un pendant la scène |
| `fin` | `texte` (la question au public) | Question au public, avec l'illustration au-dessus |
| `texte` | `texte` | Texte simple, par défaut |

Longueurs conseillées (au-delà, le texte rétrécit automatiquement, mais ça se lit moins bien) :
- `accroche` : 4 lignes max
- `point.texte` : 3 lignes max
- `versus.gauche` / `droite` : 1 ligne (« 20 ms », « 60 FPS », « Twitch »)
- `*_detail` : environ 30 caractères
