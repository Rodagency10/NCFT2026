# thierry8petstar--doublepeel

## Challenge

**ID :** 437  
**Catégorie :** misc  
**Points :** 100  
**Auteur :** thierry8petstar  
**Fichier :** `Good_Luck.jpg`  
**Format du flag :** `NCTF{...}`

> Grace D. arrive à 8 h 52, démarre son ordinateur, et 47 secondes plus tard un appel du SOC la fait partir. La photo montre son bureau tel qu'elle l'a laissé. Elle n'a tapé son mot de passe que quelques secondes. Était-il particulièrement court ?

## Résolution

Deux zones du clavier sont rétroéclairées, séparées par un bloc éteint (`5 6 r t y f g h v b`, ainsi que `- = ; /`). On lit chaque zone de gauche à droite et de haut en bas, puis on les colle. C'est le double décollage.

Zone gauche : `1 2 3 4`, `q w e`, `a s d`, `z x c`.

Zone droite : `7 8 9 0`, `u i o p`, `j k l`, `n m , .`.

Le post-it « NCTF / Investigate » rappelle seulement le format. L'arène refuse `NCTF{1qaz2wsx3edc4n7ujm8ik,9ol.0p}` et `NCTF{1234qweasdzxc7890uiopjklnm,.}`. Le mapping des touches allumées reste ouvert.
