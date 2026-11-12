# Graphes – CRUD

## Cypher – Ajout

- La clause **`CREATE`** permet d’ajouter des nœuds ainsi que des relations : <https://neo4j.com/docs/cypher-manual/current/clauses/create>
- Syntaxe :
    - Nœud simple : `CREATE ()`
    - Nœuds multiples : `CREATE (), ()`
    - Nœud avec un type (label) : `CREATE (n:Person)`
    - Nœud avec plusieurs types (labels) : `CREATE (n:Person:Swedish)`
    - Nœud avec type et propriétés :

        ```cypher
        CREATE (n:Person {name: 'Andy', title: 'Developer'})
        ```

    - Modèle (pattern) complet :

        ```cypher
        CREATE (:Person {name:'Andy'})-[:WORKS_AT]->(:Company {name: 'Neo4j'})
        ```

- La relation peut aussi être créée à partir de la recherche de nœud(s) existant(s) :

    ```cypher
    MATCH (a:Person), (b:Person)
    WHERE a.name = 'A' AND b.name = 'B'
    CREATE (a)-[:RELTYPE]->(b)
    ```

- Relation avec propriétés :

    ```cypher
    MATCH (…)
    CREATE (a)-[:RELTYPE {propriete:valeur}]->(b)
    ```

- Si un nœud avec les mêmes caractéristiques existe déjà (même type, mêmes valeurs de propriétés), `CREATE` va créer une copie du nœud.
- Si on cherche à éviter la duplication, la clause `MERGE` va auparavant valider la présence d’un nœud existant avant d’en créer un nouveau.

    ```cypher
    MERGE (:Person {name:'Andy'})
    ```

    - Souvent utilisé dans les scripts d’importation

## Cypher – Édition

- La clause **`SET`** permet d’éditer un type (label) et les propriétés d’un nœud ou d’une relation
    - <https://neo4j.com/docs/cypher-manual/current/clauses/set/>
- Elle est généralement jumelée avec l’utilisation de la clause `MATCH`

Syntaxe :

```cypher
MATCH (n …)
SET n.<propriete> = <valeur>  // ou n:Type
// optionnellement
RETURN n
```

Exemples :

```cypher
MATCH (n {name: 'Andy'})
SET n.surname = 'Taylor'
```

```cypher
MATCH (n {name: 'Andy'})
SET (CASE WHEN n.age = 36 THEN n END).worksIn = 'Malmo'
```

```cypher
MATCH (n {name: 'Andy'})
SET n.age = toString(n.age)
```

```cypher
MATCH (n {codename: '007'})
SET n.codename = null
```

Efface toutes les propriétés :

```cypher
MATCH (p {name: 'Peter'})
SET p = {}
```

Ajoute ou modifie des propriétés :

```cypher
MATCH (p {name: 'Peter'})
SET p += {age: 38, hungry: true, position: 'Entrepreneur'}
```

Remplace toutes les propriétés (pas de changement de type) :

```cypher
MATCH (at {name: 'Andy'}), (pn {name: 'Peter'})
SET at = pn
```

Remplace toutes les propriétés par les nouvelles :

```cypher
MATCH (p {name: 'Peter'})
SET p = {name: 'Peter Smith', position: 'Entrepreneur'}
```

Modifie plusieurs propriétés :

```cypher
MATCH (n {name: 'Andy'})
SET n.position = 'Developer', n.surname = 'Taylor'
```

Changement de type :

```cypher
MATCH (n {name: 'Stefan'})
SET n:German
```

## Cypher – Suppression

- La clause **`DELETE`** permet de supprimer un nœud ou une relation : <https://neo4j.com/docs/cypher-manual/current/clauses/delete/>
    - Toute relation vers un nœud doit être effacée auparavant
- La clause **`DETACH DELETE`** permet de supprimer un nœud et les relations auxquelles il est associé
- Elle est généralement jumelée avec l’utilisation de la clause `MATCH`

Syntaxe :

```cypher
MATCH (…) DELETE elementASupprimer
```

Exemples :

```cypher
MATCH (n {name: 'Andy'})
DETACH DELETE n
```

Toute relation vers le nœud `n` doit être effacée auparavant :

```cypher
MATCH (n:Person {name: 'UNKNOWN'})
DELETE n
```

```cypher
MATCH (n {name: 'Andy'})-[r:KNOWS]->()
DELETE r
```

## Exercice – Requêtes d’ajout

Utilisez la base de données du tutoriel *neo4j* sur les films (Movie Graph).

!!! warning "Attention"

    Exécutez les requêtes en ordre et assurez-vous de les prendre en note dans un fichier `.cypher`.

1. Ajoutez 3 films de votre choix (titre et tagline) en vous assurant qu’ils ne sont pas déjà présents dans la base de données
2. Pour chacun des films, ajoutez ***ensuite*** 2 acteurs qui ne sont pas déjà présents dans la base de données
3. Pour chacun des films, ajoutez ***ensuite*** les réalisateurs (`[:DIRECTED]`), à moins qu’ils ne soient déjà présents dans la base de données
4. Ajoutez ***ensuite*** les relations entre les films, les acteurs et les réalisateurs
5. Ajoutez 2 autres films, acteurs (1 par film) et réalisateurs en utilisant ***une seule requête*** de création par film.
6. Effectuez les requêtes nécessaires pour valider vos requêtes d’ajout

## Exercice – Requêtes d’édition

1. Ajoutez la durée (en minutes) sur 2 de vos films
2. Ajoutez la durée (en minutes) et l’année de réalisation sur 2 autres films
3. Ajoutez les rôles joués par les acteurs (dans la relation `ACTED_IN`) d’un de vos films
4. Modifiez l’année de réalisation d’un film de votre choix

## Exercice – Requêtes de suppression

1. Supprimez un film de votre choix. Les relations associées à ce film doivent être effacées auparavant ou Neo4j va refuser la requête
2. Supprimez un film de votre choix en supprimant du même coup ses relations.
3. Supprimez la relation entre un acteur et un film de votre choix
