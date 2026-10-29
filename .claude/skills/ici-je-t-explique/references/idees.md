# Banque d'idées : Explications Gaming & Streaming

Une idée = une question + une accroche. Quand une vidéo est publiée, ajoute une ligne dans « Déjà fait » et barre l'idée dans la liste. Les chiffres cités dans une vidéo sont à **revérifier au moment du script**.

## Réglages
- Voix off : **Lucas la génère sur ElevenLabs** à partir du script envoyé le matin, toujours avec la même voix (pas de crédits vidIQ). Si un jour on repasse sur vidIQ : voix Liam, `voiceId` `TX3LPaxmHKxFdv7VOQHJ`.
- Série : « Ici je t'explique » (champ `serie` du JSON)
- Pseudo : aucun (ces vidéos sont publiées sur un autre compte que @itsklyzen, donc aucun @ dans la vidéo)

## Déjà fait
| Date | Sujet | Fichier |
|---|---|---|
| 2026-10-29 | C'est quoi le ping ? (technique) | `videos/2026-10-29_Ping.mp4` |
| 2026-10-29 | Le délai d'un live (streaming), vidéo de test non enregistrée dans le dépôt | — |
| 2026-10-29 | C'est quoi un smurf ? (esport), vidéo de test non enregistrée dans le dépôt | — |

---

## 1. Technique : « pourquoi mon jeu fait ça ? »
- **C'est quoi le ping ?** : « Pourquoi tu lagues alors que ta connexion est rapide ? » (exemple : `exemples/ping.json`)
- **FPS : pourquoi 60 ce n'est pas pareil que 144 ?** : « Ton œil voit-il vraiment la différence ? »
- **Le stuttering** : « Ton jeu tourne à 120 FPS mais saccade quand même ? Voilà pourquoi. »
- **La hitbox** : « Tu étais SÛR de l'avoir touché… »
- **Le netcode / le rollback** : « Pourquoi tu te fais tuer derrière un mur ? »
- **Le tick rate des serveurs** : « Le serveur ne te voit pas en continu. »
- **Les shaders qui compilent** : « Pourquoi ton jeu rame les 5 premières minutes ? »
- **Le DLSS / l'upscaling** : « Ta carte graphique triche… et c'est tant mieux. »
- **Le V-Sync et le tearing** : « Ton écran se déchire en deux ? »
- **Le SSD et les chargements** : « Pourquoi plus aucun jeu ne charge comme sur PS2. »

## 2. Streaming et Twitch : « l'envers du décor »
- **Comment un streamer gagne de l'argent** : « Un sub à 4 €, il en touche combien ? » (subs, bits, pubs, sponsors : versus ou liste)
- **C'est quoi un raid ?** : « 2 000 personnes débarquent d'un coup dans ton chat. »
- **Le bitrate** : « Pourquoi ton live est flou quand ça bouge ? »
- **Affilié ou partenaire Twitch** : « Les vraies conditions pour être payé. »
- **Le délai d'un stream** : « Pourquoi le streamer répond 5 secondes après ton message ? »
- **L'algorithme de Twitch** : « Pourquoi les petits streams sont invisibles. »
- **Le setup d'un streamer** : « OBS, scènes, overlays : comment ça marche en 1 min. »
- **Les clips et les VOD** : « Pourquoi ce clip a explosé et pas le live. »
- **Les drops Twitch** : « Pourquoi regarder un live te donne des items en jeu. »
- **Le subathon** : « Le stream qui ne s'arrête jamais tant qu'on s'abonne. »

## 3. Business du jeu vidéo : « pourquoi c'est si cher ? »
- **Pourquoi un jeu coûte 80 €** : « Où va vraiment ton argent ? »
- **Les jeux free-to-play** : « Gratuit… mais comment ils gagnent des milliards ? »
- **Les loot boxes** : « Pourquoi c'est interdit dans certains pays ? »
- **Le battle pass** : « Pourquoi tu te sens obligé de le finir. »
- **L'early access** : « Payer pour un jeu pas fini, c'est normal ? »
- **Les remasters et les remakes** : « Quelle différence, au juste ? »
- **Le crunch** : « Pourquoi les jeux sortent buggés. »
- **Les jeux AAA, AA et indés** : « Les lettres, ça veut dire quoi ? »

## 4. Esport et compétition
- **Comment marche le classement Elo / MMR** : « Pourquoi tu stagnes toujours au même rang. »
- **C'est quoi un smurf ?** : « Le pro qui joue contre toi en Bronze. »
- **Les salaires en esport** : « Joueur pro, ça rapporte combien ? »
- **La méta** : « Pourquoi tout le monde joue le même perso. »
- **Les patchs et les nerfs** : « Ton main a été nerf… mais pourquoi ? »
- **Le format d'un tournoi** : « Bracket, poules, double élimination en 1 min. »

## 5. Culture gaming : « ça vient d'où ? »
- **Pourquoi on dit « GG »** : « Et pourquoi c'est parfois une insulte. »
- **C'est quoi un speedrun ?** : « Finir un jeu en 5 minutes en passant à travers les murs. »
- **Les glitches légendaires** : « Le bug qui est devenu une technique pro. »
- **Les easter eggs** : « Le premier secret caché dans un jeu vidéo. »
- **Les mots du gaming** : « Noob, tryhard, toxic : les vraies définitions. » (série possible, un mot par vidéo)
- **Pourquoi les jeux ont des « boss »** : « D'où vient l'idée du gros méchant de fin de niveau ? »
- **La rétrocompatibilité** : « Pourquoi tes vieux jeux ne marchent plus. »

## 6. Santé et bonnes pratiques du joueur
- **La lumière bleue et le sommeil** : « Jouer avant de dormir, vraiment mauvais ? »
- **Le tilt** : « Pourquoi tu perds 5 games d'affilée quand t'es énervé. »
- **La posture et le poignet** : « Le réflexe que font tous les pros. »
- **Les arnaques gaming** : « Faux skins gratuits, faux giveaways : comment les repérer. »

---

## Formats qui marchent bien
- **Question → réponse surprenante** (l'accroche pose la question, la réponse arrive à la scène 2 ou 3).
- **Mythe ou réalité** : « Plus de FPS = meilleur joueur ? » avec une scène `versus`.
- **Le chiffre fou** : on ouvre sur une scène `chiffre`.
- **Le top 3** : une scène `liste` au milieu.
- **Série en plusieurs parties** : on finit par « partie 2 si vous voulez » pour faire réagir.
