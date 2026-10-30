---
name: ici-je-t-explique
description: "« Ici je t'explique » : vidéos explicatives animées sur le gaming et le streaming (format vertical 1080x1920, 45-60 s, voix off + texte animé + sous-titres + musique originale). Trouve des idées de sujets, écrit le script, génère la voix et rend la vidéo prête à publier. À utiliser dès que Lucas veut « expliquer un truc » en vidéo, cherche une idée de vidéo gaming/stream/Twitch/esport, demande « c'est quoi le ping / un drop / le lag / un speedrun… en vidéo », veut une série pédagogique ou « Ici je t'explique », ou quand la tâche planifiée demande la vidéo du jour, même s'il ne dit pas « explicative ». Pas pour les edits « Welcome to » pays/villes (klyzen-edits-motion) ni le montage de clips de live (klyzen-studio-crea)."
---

# Ici je t'explique : vidéos explicatives gaming et streaming

Tu produis des petites vidéos qui expliquent **une seule notion** du gaming ou du streaming en 45-60 secondes. Chaque vidéo associe :
- une **voix off** qui explique,
- un **texte animé** à l'écran qui montre les mots-clés (et pas tout le texte lu),
- des **sous-titres** synchronisés avec la voix (beaucoup regardent sans le son),
- une **musique originale** discrète, qui baisse quand la voix parle.

Lucas publie ces vidéos sur un compte dédié, « Ici je t'explique », différent de @itsklyzen, sur TikTok, Reels et YouTube Shorts : ne mets donc aucun @ ni pseudo dans la vidéo, ni dans le champ `pseudo` du JSON. Son public est jeune et francophone. Le ton : un pote qui s'y connaît, tutoiement, phrases courtes, zéro jargon non expliqué.

## Déroulé

### 1. Choisir le sujet
Si Lucas n'a pas d'idée, ouvre `references/idees.md` et propose **3 sujets**, chacun avec son accroche, en variant les catégories. Privilégie ceux qui ne sont pas cochés dans le tableau de suivi. Un bon sujet :
- tient en **une question** (« C'est quoi le ping ? », « Pourquoi les jeux coûtent 80 € ? ») ;
- concerne beaucoup de joueurs ou de viewers ;
- a une réponse **surprenante ou utile** à retenir.

S'il a déjà un sujet, passe directement à l'étape 2.

### 2. Vérifier les faits
Les chiffres et les dates doivent être vrais : une erreur dans les commentaires fait perdre toute crédibilité. Vérifie tout fait daté ou chiffré avec WebSearch, surtout ce qui change vite (prix, records, règles Twitch, revenus). Si un chiffre est incertain, arrondis-le (« plus de 100 millions ») ou retire-le.

### 3. Écrire le script en scènes
Écris un fichier `scenes.json` (format complet dans `references/format_scenes.md`, exemple complet dans `exemples/ping.json`). La structure qui marche :

| Scène | Rôle | Durée visée |
|---|---|---|
| `accroche` | Une question ou un fait choc qui donne envie de rester. Les 2 premières secondes décident de tout. | 5-8 s |
| 2 à 4 scènes de contenu (`point`, `chiffre`, `exemple`, `versus`, `liste`) | Une idée par scène, du plus simple au plus surprenant | 7-12 s chacune |
| `fin` | Une question au public (pour les commentaires) + un appel à s'abonner | 5-7 s |

Règles d'écriture :
- **`voix`** = ce qui est lu. Écris comme on parle : « t'as », « en gros », des phrases de 8 à 15 mots. Au total, **650 à 850 caractères** de voix pour 45-60 s (à environ 14,5 caractères par seconde).
- **`texte`** = ce qui s'affiche en gros : **2 à 7 mots**, jamais la phrase lue en entier. Mets 1 ou 2 mots-clés entre `*astérisques*` pour les passer en jaune : ils apparaissent avec un petit éclat.
- **Chaque exemple devient une mini-vidéo.** Dès que la voix donne un exemple concret (« à 200 ms, l'ennemi se téléporte », « sur 4 €, il touche 2 € », « tu écris, il répond 5 s plus tard »), fais une scène `exemple` : une petite animation que tu inventes, avec des persos et des objets qui jouent la situation (tir, téléportation, pièce qui passe de main en main, bulle de dialogue...). Pour comparer deux cas, mets deux fenêtres l'une sous l'autre. Le spectateur doit comprendre l'exemple même sans le son. Tout est expliqué dans `references/saynetes.md` (acteurs, actions, conseils de mise en scène, exemples à copier). Vise au moins une scène `exemple` par vidéo : c'est le moment qu'on retient.
- **Une image animée par scène.** C'est ce qui rend la vidéo vivante : on doit *voir* ce que la voix dit. Si la voix dit « aller-retour », mets `aller_retour` (des flèches qui partent et reviennent). Si elle parle d'argent, des `pieces` tombent. Si elle parle du chat Twitch, un `chat` défile. Choisis dans `references/illustrations.md` (13 animations et 36 icônes, avec une table « si on parle de X → mets Y »). En `versus`, mets une icône dans chaque carte (`gauche_icone`, `droite_icone`). En `liste`, mets une icône par élément (`icones`). Évite de réutiliser la même animation deux fois dans une vidéo.
- Écris les nombres en chiffres dans `texte` (« 20 ms ») et en toutes lettres dans `voix` (« vingt millisecondes »), sinon la synthèse vocale peut mal les lire.
- Pas d'anglicisme sans explication : si tu dis « hitbox », la phrase d'après dit ce que c'est.
- Varie les types de scènes : jamais deux `point` de suite si un `chiffre` ou un `versus` peut le remplacer.

Montre le script à Lucas (le tableau des scènes avec voix, texte et illustration) **avant de générer la voix** : la voix coûte des crédits ElevenLabs, une relecture ne coûte rien. (En mode automatique, tu relis toi-même : voir plus bas.)

### 4. Générer la voix off
La voix se fait **avec le connecteur ElevenLabs** (outils `mcp__ElevenLabs__creative_*`, à charger avec ToolSearch si besoin), toujours avec la même voix : **Marcel - French touch**, `voice_id` `kENkNtk0xyzG09WW40xE` (noté dans `references/idees.md`, section « Réglages »).

**Écrire pour ElevenLabs.** Il lit exactement ce qui est écrit, donc dans `voix` : nombres et unités en toutes lettres (« vingt millisecondes », jamais « 20 ms »), pas de sigles qu'il risque de mal prononcer (« images par seconde » plutôt que « FPS » ; si un sigle est indispensable, écris-le comme il se dit, ex. « F.P.S. »), pas d'émojis ni de symboles (€, %, →) : écris « euros », « pour cent ».

1. `python3 $S scenes.json --script` affiche le texte à lire, un paragraphe par scène séparés par une ligne vide (ElevenLabs y marque une petite pause, sur laquelle le rendu cale les changements de scène). Enregistre-le dans `script_voix.txt`.
2. `creative_generate_speech` avec **tout le script d'un coup** (`prompt` = sortie de `--script`), `voice_id` `kENkNtk0xyzG09WW40xE`, `model_id` `eleven_v4`, `generations_count` laissé par défaut (2 prises). Un seul appel : ne le relance jamais pour réessayer, chaque appel coûte des crédits.
3. `creative_get_flow_run_status` (avec le `flow_id` et les `session_ids` reçus), en attendant `poll_after_seconds` entre deux appels, jusqu'à `all_completed` ou `has_failures`.
4. `creative_get_generations` sur les prises pour récupérer leur `full_res_url`, puis télécharge-les (`curl -L -o prise1.mp3 <url>`). Garde celle dont la durée tombe dans 45-60 s (`--timing` donne la durée totale) et qui cale le mieux (ligne « Calage sur les pauses » de `--timing`) ; enregistre-la sous `voix.mp3`.
5. Si moins de la moitié des changements de scène sont calés, regarde les `--still` aux coupures et, si besoin, fixe `debut`/`fin` à la main.

**Si le connecteur ElevenLabs n'est pas disponible** (outils introuvables, erreur d'accès, crédits épuisés) : n'insiste pas. Donne à Lucas le script dans un bloc de code pour qu'il le colle lui-même dans ElevenLabs avec la voix Marcel, en MP3, et qu'il te renvoie le fichier dans la conversation. Sans voix, le rendu marche aussi (texte, sous-titres et musique seulement, au débit estimé d'une voix).
vidIQ ne sert que si Lucas le demande explicitement (voix Liam, `voiceId` `TX3LPaxmHKxFdv7VOQHJ`, outils `vidiq_voiceover_generate` puis `vidiq_job_poll`).

### 5. Rendre la vidéo
```bash
S=<dossier de ce skill>/scripts/render_explication.py
python3 $S scenes.json --voix voix.mp3 --timing                     # découpage des scènes et durée totale
python3 $S scenes.json --voix voix.mp3 --still 2 12 25 40 --out apercu.png   # images fixes à vérifier
python3 $S scenes.json --voix voix.mp3 --out video.mp4              # rendu final (~1 min)
```
Le script cale automatiquement chaque scène sur la voix, au prorata de la longueur de son texte `voix`. Il génère aussi la musique et les whooshes, baisse la musique sous la voix, normalise le son à -14 LUFS et vérifie la taille (moins de 20 Mo).

Regarde toujours les images de `--still` avant le rendu final : texte coupé, chevauchement, mot-clé mal placé… Si une scène est trop chargée, raccourcis son `texte` plutôt que de bricoler le script.

Si un changement de scène tombe au mauvais moment par rapport à la voix (par exemple une phrase très lente), fixe `debut` et `fin` à la main dans le JSON pour **toutes** les scènes : le script utilise alors ces temps tels quels.

### 6. Livrer
Tout va dans le dépôt GitHub `itsklyzen-hub/ici-je-t-explique` (jamais dans `welcome-to-videos`) :
- la vidéo : `videos/AAAA-MM-JJ_<Sujet>.mp4` (moins de 20 Mo). Son lien direct est `https://raw.githubusercontent.com/itsklyzen-hub/ici-je-t-explique/main/videos/<fichier>` ;
- le script et la voix, pour pouvoir refaire la vidéo : `explications/AAAA-MM-JJ_<sujet>/scenes.json` et `voix.mp3` ;
- la légende : `explications/AAAA-MM-JJ_<sujet>/legende.txt`.
- Envoie la vidéo à Lucas, avec la **légende** et une idée de **suite** (« partie 2 : comment baisser son ping sur console »).
- **Format de la légende** (toujours le même, court, pour que Lucas la colle vite) : `Ici je t'explique : <titre de la vidéo>`, une ligne vide, puis exactement 5 hashtags liés au sujet (1 ou 2 généraux comme #gaming ou #twitch, le reste propre au sujet). Rien d'autre : pas de phrase d'accroche, pas d'émoji. Exemple :
  ```
  Ici je t'explique : c'est quoi une loot box ?

  #lootbox #gaming #jeuxvideo #skins #gacha
  ```
- Coche le sujet dans `references/idees.md` (date et lien).

## Mode automatique : la vidéo du jour
Une tâche planifiée lance ce skill tous les jours vers 5 h (heure de Paris) pour créer **une vidéo différente chaque jour**, sans personne pour relire. Dans ce mode :
1. **Sujet** : lis le tableau « Déjà fait » de `references/idees.md` et prends une idée qui n'y est pas. Change de catégorie par rapport aux 2 dernières vidéos. Si toutes les idées sont faites, invente un nouveau sujet du même genre et ajoute-le à la banque.
2. **Relecture à ta place** : au lieu de montrer le script à Lucas, relis-le toi-même avec ses yeux : faits vérifiés, 650-850 caractères de voix, au moins une scène `exemple` avec une mini-vidéo, une illustration par scène, pas de @, et les règles d'écriture pour ElevenLabs de l'étape 4 (nombres en lettres, pas de symboles, sigles écrits comme ils se disent).
3. **Voix** : génère-la toi-même avec le connecteur ElevenLabs (étape 4, voix Marcel). Pas besoin d'attendre Lucas.
4. **Rendu** : `--voix voix.mp3 --timing`, `--still` sur au moins un instant par scène et aux changements de scène, corrections, puis rendu final.
5. **Livraison du matin** : commit et push sur `main` du dépôt `ici-je-t-explique` (`videos/AAAA-MM-JJ_<Sujet>.mp4`, `explications/AAAA-MM-JJ_<sujet>/scenes.json`, `script_voix.txt`, `voix.mp3`, `legende.txt`, et la ligne ajoutée dans « Déjà fait »). Puis envoie à Lucas la vidéo (SendUserFile) avec son lien direct, et la légende (format de l'étape 6) dans un bloc de code.

**Si le connecteur ElevenLabs n'est pas disponible** dans la tâche planifiée : rends la vidéo sans voix (`videos/AAAA-MM-JJ_<Sujet>_sans_voix.mp4`), pousse-la avec le reste, et envoie à Lucas le script dans un bloc de code (à coller dans ElevenLabs avec la voix Marcel, export MP3, à renvoyer dans cette conversation). Quand son MP3 arrive : refais le rendu avec `--voix`, vérifie le calage et quelques `--still`, enregistre `voix.mp3` et la vidéo finale, supprime la version `_sans_voix`, commit + push et renvoie-lui la vidéo finale avec son lien direct.
Ne publie jamais rien sur les réseaux : c'est Lucas qui publie.

## Charte visuelle (déjà intégrée au rendu)
Les illustrations sont des pictos néon dessinés par le script (`scripts/illustrations.py`). Pour ajouter une icône ou une animation qui manque, ajoute une fonction dans ce fichier, en suivant le modèle des autres, plutôt que d'utiliser une image trouvée sur internet (question de droits et de cohérence visuelle).
Fond violet nuit avec une grille néon façon synthwave. Texte blanc, contour sombre, mots-clés en jaune `#FFD60A`, accents cyan `#00E5FF` et rose `#FF2E88`. Police Inter Black. En haut : une barre de progression, la pastille de série (« Ici je t'explique », champ `serie`) et le titre. Les sous-titres sont placés au-dessus de la zone couverte par l'interface TikTok. Pour une série spéciale, on peut changer les couleurs avec le champ `couleurs` du JSON. Garde les mêmes réglages d'une vidéo à l'autre : c'est ce qui rend la série reconnaissable.

## Ce qu'il faut éviter
- Les logos, les captures de jeux et les personnages sous copyright dans la vidéo : le rendu reste en texte et en formes.
- Les musiques connues : la musique est synthétisée, donc libre de droits.
- Les sujets polémiques ou les attaques contre un streamer précis : on explique, on ne clashe pas.
- Plus d'une notion par vidéo : si le sujet déborde, fais-en une série (« partie 1 », « partie 2 »).
