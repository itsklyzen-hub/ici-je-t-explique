---
name: ici-je-t-explique
description: « Ici je t'explique » : vidéos explicatives animées sur le gaming et le streaming (format vertical 1080x1920, 45-60 s, voix off + texte animé + sous-titres + musique originale). Trouve des idées de sujets, écrit le script, génère la voix et rend la vidéo prête à publier. À utiliser dès que Lucas veut « expliquer un truc » en vidéo, cherche une idée de vidéo gaming/stream/Twitch/esport, demande « c'est quoi le ping / un drop / le lag / un speedrun… en vidéo », veut une série pédagogique ou « Ici je t'explique », ou quand la tâche planifiée demande la vidéo du jour, même s'il ne dit pas « explicative ». Pas pour les edits « Welcome to » pays/villes (klyzen-edits-motion) ni le montage de clips de live (klyzen-studio-crea).
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

Montre le script à Lucas (le tableau des scènes avec voix, texte et illustration) **avant de générer la voix** : la voix coûte des crédits, une relecture ne coûte rien.

### 4. Générer la voix off
Avec les outils vidIQ (chercher `vidiq_voiceover` avec ToolSearch si besoin) :
1. `vidiq_voiceover_list_voices` : si Lucas a une voix perso (`isCustom=true`), prends-la. Sinon, choisis une voix française dynamique et garde la même d'une vidéo à l'autre (note son `voiceId` dans `references/idees.md`, section « Réglages »).
2. `vidiq_voiceover_generate` avec **toute la voix d'un coup** : les champs `voix` des scènes, dans l'ordre, séparés par un espace. Un seul appel coûte moins cher que des appels par scène.
3. `vidiq_job_poll` jusqu'à « completed », puis télécharge le MP3 (`curl -L -o voix.mp3 <url>`).

**Par défaut, la voix est faite par Lucas sur ElevenLabs** (pas de crédits vidIQ) : il colle le script dans ElevenLabs, toujours avec la même voix, et t'envoie le MP3. ElevenLabs lit exactement ce qui est écrit, donc dans `voix` : nombres et unités en toutes lettres (« vingt millisecondes », jamais « 20 ms »), pas de sigles qu'il risque de mal prononcer (« images par seconde » plutôt que « FPS » ; si un sigle est indispensable, écris-le comme il se dit, ex. « F.P.S. »), pas d'émojis ni de symboles (€, %, →) : écris « euros », « pour cent ». `python3 $S scenes.json --script` affiche le texte à lire, un paragraphe par scène, prêt à copier. Avec sa voix, le rendu cale chaque changement de scène sur ses pauses entre les paragraphes. Vérifie la ligne « Calage sur les pauses » de `--timing` : si moins de la moitié des changements sont calés, regarde les `--still` aux coupures et, si besoin, fixe `debut`/`fin` à la main. Sans voix, le rendu marche aussi (texte, sous-titres et musique seulement, au débit estimé d'une voix).
vidIQ ne sert que si Lucas le demande explicitement.

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
- Envoie la vidéo à Lucas, avec une **légende TikTok** (accroche + 3-5 hashtags : #gaming #twitch #apprendresurtiktok + 1-2 propres au sujet) et une idée de **suite** (« partie 2 : comment baisser son ping sur console »).
- Coche le sujet dans `references/idees.md` (date et lien).

## Mode automatique : la vidéo du jour
Une tâche planifiée lance ce skill tous les jours vers 5 h (heure de Paris) pour créer **une vidéo différente chaque jour**, sans personne pour relire. Lucas fait la voix lui-même à son réveil. Dans ce mode :
1. **Sujet** : lis le tableau « Déjà fait » de `references/idees.md` et prends une idée qui n'y est pas. Change de catégorie par rapport aux 2 dernières vidéos. Si toutes les idées sont faites, invente un nouveau sujet du même genre et ajoute-le à la banque.
2. **Relecture à ta place** : au lieu de montrer le script à Lucas, relis-le toi-même avec ses yeux : faits vérifiés, 650-850 caractères de voix, au moins une scène `exemple` avec une mini-vidéo, une illustration par scène, pas de @. La voix sera lue par ElevenLabs : applique les règles d'écriture de la voix de l'étape 4 (nombres en lettres, pas de symboles, sigles écrits comme ils se disent).
3. **Vidéo sans voix** : rends la vidéo tout de suite sans voix (`--timing`, `--still` sur au moins un instant par scène, corrections, puis rendu final). C'est la version d'aperçu.
4. **Livraison du matin** : commit et push sur `main` du dépôt `ici-je-t-explique` (`videos/AAAA-MM-JJ_<Sujet>_sans_voix.mp4`, `explications/AAAA-MM-JJ_<sujet>/scenes.json`, `script_voix.txt`, `legende.txt`, et la ligne ajoutée dans « Déjà fait »). Puis envoie à Lucas :
   - la vidéo (SendUserFile) ;
   - dans ta réponse, **le script pour ElevenLabs dans un bloc de code** (sortie de `--script` : un paragraphe par scène, séparés par une ligne vide, ce qui fait marquer une petite pause à ElevenLabs), pour qu'il le colle d'un geste, avec la durée visée et un rappel : garder la même voix que d'habitude, exporter en MP3, et renvoyer le MP3 dans cette même conversation ;
   - la légende TikTok, elle aussi dans un bloc de code.
5. **Quand Lucas envoie son MP3** (dans la même conversation) : refais le rendu avec `--voix`, vérifie le calage (`--timing`) et quelques `--still` aux changements de scène, puis enregistre `voix.mp3` et `videos/AAAA-MM-JJ_<Sujet>.mp4` (version finale). Supprime la version `_sans_voix`, fais un commit + push et renvoie-lui la vidéo finale avec son lien direct.
Ne publie jamais rien sur les réseaux : c'est Lucas qui publie.

## Charte visuelle (déjà intégrée au rendu)
Les illustrations sont des pictos néon dessinés par le script (`scripts/illustrations.py`). Pour ajouter une icône ou une animation qui manque, ajoute une fonction dans ce fichier, en suivant le modèle des autres, plutôt que d'utiliser une image trouvée sur internet (question de droits et de cohérence visuelle).
Fond violet nuit avec une grille néon façon synthwave. Texte blanc, contour sombre, mots-clés en jaune `#FFD60A`, accents cyan `#00E5FF` et rose `#FF2E88`. Police Inter Black. En haut : une barre de progression, la pastille de série (« Ici je t'explique », champ `serie`) et le titre. Les sous-titres sont placés au-dessus de la zone couverte par l'interface TikTok. Pour une série spéciale, on peut changer les couleurs avec le champ `couleurs` du JSON. Garde les mêmes réglages d'une vidéo à l'autre : c'est ce qui rend la série reconnaissable.

## Ce qu'il faut éviter
- Les logos, les captures de jeux et les personnages sous copyright dans la vidéo : le rendu reste en texte et en formes.
- Les musiques connues : la musique est synthétisée, donc libre de droits.
- Les sujets polémiques ou les attaques contre un streamer précis : on explique, on ne clashe pas.
- Plus d'une notion par vidéo : si le sujet déborde, fais-en une série (« partie 1 », « partie 2 »).
