# MongoDB – Exercices de révision

Ces exercices utilisent la base de données des restaurants de New York.

1. Écrivez une requête MongoDB pour lister les restaurants par type de cuisine (ordre croissant) et l'arrondissement par ordre décroissant.
2. Écrivez une requête MongoDB pour trouver l'identifiant, le nom, l'arrondissement et la cuisine des restaurants qui préparent des plats autres que américains (`"American"`) et chinois (`"Chinese"`).
3. Écrivez une requête MongoDB qui sélectionnera l'identifiant, le nom et les notes (*grades*) du restaurant pour les restaurants qui ont au moins une évaluation avec un score d'exactement 7.
4. Analysez la requête précédente avec `.explain('executionStats')`, écrivez la requête pour créer l'index manquant, puis analysez la requête à nouveau.
5. Écrivez une requête pour renommer le « Parkside Restaurant » en « Lakeside Restaurant ».
6. Écrivez une requête pour effacer les restaurants italiens de Staten Island.
7. Écrivez une requête MongoDB pour trouver le nombre de restaurants pour chaque combinaison cuisine et arrondissement.
8. Écrivez une requête MongoDB pour trouver le nombre d'évaluations de restaurants qui ont le même score, puis ordonnez les scores du plus attribué au moins attribué (indice : utilisez `$unwind` pour pivoter vers les évaluations (`grades`)).
