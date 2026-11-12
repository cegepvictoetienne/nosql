# Graphes – Clauses et fonctions

## Clauses et fonctions dans Neo4j

- Clauses (en majuscules):
    - `MATCH`, `WHERE`, `ORDER BY`, `SKIP`, `LIMIT`, `UNWIND`
- Fonctions (en minuscules):
    - Regroupement :
        - Somme, moyenne, min, max, dénombrement
    - Mathématiques :
        - Arrondissement, valeurs planchers, plafond
    - Prédicats (retournent vrai ou faux) :
        - `all`, `any`, `exists`, `none`, `single`
    - Temporelles :
        - manipulation des dates et heures
    - Spatiales :
        - `distance`, `point`

## `MATCH`

- Clause de base permettant de définir le modèle (« pattern ») recherché.
- Syntaxe :
    - Tous les nœuds : `MATCH (n) RETURN n`
    - Nœuds avec un type/étiquette : `MATCH (movie:Movie) RETURN movie.title`
    - Nœuds interreliés :

        ```cypher
        MATCH (n1 {name: 'Oliver Stone'})--(n2)
        RETURN n2
        ```

        ```cypher
        MATCH (:Person {name: 'Oliver Stone'})--(n2:Movie)
        RETURN n2
        ```

    - Définir le sens de la relation (`-->` ou `<--`) :

        ```cypher
        MATCH (:Person {name: 'Oliver Stone'})-->(n2)
        RETURN n2
        ```

    - Réutiliser la relation de la requête :

        ```cypher
        MATCH (:Person {name: 'Oliver Stone'})-[r]->(movie)
        RETURN type(r)
        ```

    - Préciser la nature (le type) de la relation entre les nœuds recherchés :

        ```cypher
        MATCH (actor)-[:ACTED_IN]->(m:Movie {title: 'Wall Street'})
        RETURN actor.name
        ```

        ou :

        ```cypher
        MATCH (person)-[:ACTED_IN|:DIRECTED]->(m:Movie)
        RETURN person.name
        ```

- Souvent utilisée en combinaison avec la clause `WHERE` qui permet d’ajouter des restrictions aux valeurs recherchées.
- Documentation : <https://neo4j.com/docs/cypher-manual/current/clauses/match/>

- Cette clause suivie de `CREATE` permet de créer des relations:

```cypher
MATCH (p1:Person {name: 'Charlie Sheen'}), (p2:Person {name: 'Rob Reiner'})
CREATE (p1)-[:TYPE]->(p2)
```

- Relations multiples:

```cypher
MATCH (charlie {name: 'Charlie Sheen'})-[:ACTED_IN]->(movie)<-[:DIRECTED]-(director)
RETURN movie.title, director.name
```

- Définition du nombre de bonds :

```cypher
-[:TYPE*minHops..maxHops]->
```

- Chemin le plus court (*shortest path*) :

```cypher
MATCH (p1:Person {name: 'Charlie Sheen'}), (p2:Person {name: 'Martin Sheen'}), p = shortestPath((p1)-[*]-(p2))
RETURN p
```

## `WHERE`

- La clause `WHERE` permet de définir des contraintes additionnelles sur des éléments recherchés
- <https://neo4j.com/docs/cypher-manual/current/clauses/where/>
- Peut être utilisé avec les mots-clés `AND`, `OR`, `XOR` ou `NOT`
- Fréquemment utilisée pour filtrer les nœuds ou les relations en fonction de leurs propriétés
- Permet aussi de filtrer sur l’existence (ou la non-existence) d’une propriété sur un nœud ou une relation.
- Permet l’utilisation d’expressions régulières

## `ORDER BY`

- Permet de trier les données retournées
    - <https://neo4j.com/docs/cypher-manual/current/clauses/order-by/>
- Exemples :

```cypher
MATCH (n)
RETURN n.name, n.age
ORDER BY n.name
```

```cypher
MATCH (n)
RETURN n.name, n.age
ORDER BY n.age, n.name
```

```cypher
MATCH (n)
RETURN n.name, n.age
ORDER BY n.name DESC
```

## `SKIP`

- Permet de définir à partir de quel élément retourner les résultats
    - <https://neo4j.com/docs/cypher-manual/current/clauses/skip/>
- Exemple :

```cypher
MATCH (n)
RETURN n.name
ORDER BY n.name
SKIP 10
```

## `LIMIT`

- Permet de limiter le nombre de résultats retournés par la requête
    - <https://neo4j.com/docs/cypher-manual/current/clauses/limit/>
- Exemple :

```cypher
MATCH (n)
RETURN n.name
ORDER BY n.name
SKIP 10
LIMIT 5
```

## `UNWIND`

- Permet d’étendre une liste en séquence d’enregistrements
    - <https://neo4j.com/docs/cypher-manual/current/clauses/unwind/>

```cypher
CREATE ( {tableau:['a', 'b']}),
       ( {tableau:['c']});

MATCH(n)
UNWIND n.tableau AS v
RETURN v;
```

Résultat :

|  | v |
|---|---|
| 1 | "a" |
| 2 | "b" |
| 3 | "c" |

## Fonctions de regroupement

- Les fonctions de regroupement (agrégation) permettent une analyse statistique de l’information contenue dans une base de données
    - <https://neo4j.com/docs/cypher-manual/current/functions/#header-query-functions-aggregating>

| Fonction | Cypher |
|---|---|
| Moyenne | `avg()` |
| Dénombrement | `count()` |
| Somme | `sum()` |
| Minimum | `min()` |
| Maximum | `max()` |
| Écart type | `stDev()` |

- Exemples :

```cypher
MATCH (n:Person)
RETURN avg(n.age)
```

```cypher
MATCH (n {name: 'Jack Black'})-->(x)
RETURN count(x)
```

Une expression qui utilise des fonctions de regroupement est appelée une expression de regroupement (ou d'agrégation).

## Clé de regroupement

- Si une requête Cypher combine des expressions de regroupement avec des expressions qui ne le sont pas, ces dernières sont considérées comme des clés de regroupement.

- <https://neo4j.com/docs/cypher-manual/current/functions/aggregating/#grouping-keys>

Exemples :

```cypher
// Nb films par année
MATCH (n:Movie)
RETURN n.released, count(*);

// Évaluation moyenne par critique
MATCH (p:Person)-[r:REVIEWED]->(:Movie)
RETURN p.name, avg(r.rating)
```

## Fonctions mathématiques

- Les fonctions mathématiques standard disponibles :
    - <https://neo4j.com/docs/cypher-manual/current/functions/mathematical-numeric/>
    - `rand()`
    - `ceil()`
    - `floor()`
    - `round()`
    - `abs()`
    - `sign()`
- Les fonctions logarithmiques et trigonométriques sont aussi disponibles:
    - <https://neo4j.com/docs/cypher-manual/current/functions/mathematical-logarithmic/>
    - <https://neo4j.com/docs/cypher-manual/current/functions/mathematical-trigonometric/>

## Fonctions prédicats

- Les prédicats sont des fonctions qui retournent vrai ou faux (fonctions booléennes)
    - Les prédicats servent à filtrer les requêtes ou comme expression dans les `RETURN`
    - <https://neo4j.com/docs/cypher-manual/current/functions/predicate/>
- `none()`
- `any()`
- `all()`

```cypher
MATCH p = (:Person)--(:Person)
WHERE all(n IN nodes(p) WHERE n.born < 1975)
RETURN p;
```

- `exists()` – existence d’une relation

```cypher
MATCH (p:Person)
RETURN p.name,
       exists((p)-[:ACTED_IN]->()) AS has_acted
```

- Utilisez `IS NOT NULL` pour tester l’existence d’une propriété
- `isEmpty()` – Tableau et chaine de caractères

```cypher
MATCH (p:Person)
WHERE isEmpty(p.instructions_livraison)
RETURN p.name
```

## Fonctions temporelles

### `date()` – date calendrier

- `date("2025-02-18")` (format ISO 8601)
- `date({year: 2025, month: 2, day: 18})`

```cypher
CREATE (n:Label)
SET n.date = date("2025-02-18")
```

- <https://neo4j.com/docs/cypher-manual/current/values-and-types/temporal/>
- `date()` sans arguments retourne la date courante selon le fuseau horaire configuré pour le serveur
- UTC dans le conteneur neo4j de devilbox

```cypher
RETURN apoc.date.systemTimezone()
```

### `datetime()` – moment

- `datetime("2026-03-17T10:42:14")` (format ISO 8601)
- `datetime()` sans argument retourne la date courante selon le fuseau horaire configuré pour le serveur
- Le fuseau horaire fait partie du `datetime()`, contrairement au `date()`
    - Pour cette raison, pour s’assurer la gestion correcte sur plusieurs fuseaux horaires, `datetime()` est habituellement utilisé dans les bases de données en production même si seulement la partie calendrier est utilisée.

### `duration()` – durée dans le temps

- `duration({days: 10, hours:12})`
- `duration("P10DT12H")` (ISO 8601 duration format)
- <https://neo4j.com/docs/cypher-manual/current/functions/temporal/duration/>

## Fonctions spatiales

- Primitive `POINT`
    - 2D ou 3D
    - Cartésien (x,y,z) ou coordonnées géographiques (latitude, longitude, élévation - WGS84)
    - `point({x:3.5, y:7.6, z:-8.4})`
    - `point({longitude: 56.7, latitude: 12.78})`
- Fonction `point.distance()`

```cypher
WITH
  point({x: 2.3, y: 4.5}) AS p1,
  point({x: 1.1, y: 5.4}) AS p2
RETURN point.distance(p1,p2)
```

- <https://neo4j.com/docs/cypher-manual/current/functions/spatial/>

## Exercice, partie 1

- Utilisez le projet « **Contact Tracing** » disponible sur <https://sandbox.neo4j.com/> (plus bas dans la page)
- OU recréez la base de données à partir des commandes cypher ici:
    - <https://github.com/SebastienTrottierCEGEP/Megadonnees/blob/main/contact_tracing_5.0_dump.cypher>

```cypher
CREATE DATABASE contact
:USE contact
```

- Copiez-collez le contenu du fichier cypher dans Neo4j Desktop ou exécutez-le dans VS Code
- Il y a 5615 personnes dans le graphe

- Trouvez les requêtes permettant de trouver les résultats aux questions suivantes :
    - Liste des personnes recensées par l’étude
    - Nombre de personnes recensées
    - Liste des personnes malades
    - Nombre de personnes regroupées selon le statut de santé
    - Liste des endroits visités par Rachel Valentine
    - Nombre de visites effectuées par Rachel Valentine

## Exercice, partie 2

- Toujours avec le projet « Contact Tracing », trouvez les requêtes permettant de trouver les résultats aux questions suivantes :
    - Liste des personnes ayant visité un endroit en commun avec Rachel Valentine
    - Liste des personnes ayant visité un endroit en commun avec Rachel Valentine, triées en ordre alphabétique. Ne retourner que le nom, et le statut de santé des personnes.
    - Affichez les 50 premiers résultats de la requête précédente
    - Affichez les 50 résultats suivants (51 à 100)
    - Liste des visites ayant eu lieu (date de début) en mai 2020
    - Durée moyenne des visites par endroit
- Terminé?
    - Étudiez les requêtes proposées dans le guide du projet

Ligne de commande :

```cypher
:play https://guides.neo4j.com/sandbox/contact-tracing/index.html
```
