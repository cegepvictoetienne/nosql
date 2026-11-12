# Graphes – Optimisation et modèles

## Optimisation

Tout comme les autres SGBD, Neo4j met en place des fonctionnalités pour optimiser les traitements.

### Index

Différents types sont disponibles :

- **Plage** (« range ») – celui par défaut :

```cypher
CREATE INDEX range_index_nom FOR (n:Personne) ON (n.age)
```

<https://neo4j.com/docs/cypher-manual/current/administration/indexes-for-search-performance/>

Couvre :

| Opération | Exemple |
|---|---|
| Equality check | `n.prop = value` |
| List membership check | `n.prop IN list` |
| Existence check | `n.prop IS NOT NULL` |
| Range search | `n.prop > value` |
| Prefix search | `STARTS WITH` |

- **Texte** – pour les opérations sur les chaînes de caractères (`CONTAINS`, `STARTS WITH`, `ENDS WITH`)

```cypher
CREATE TEXT INDEX … FOR (n:Personne) ON (n.nom)
```

<https://neo4j.com/docs/cypher-manual/current/indexes/search-performance-indexes/create-indexes/#create-text-index>

- **Point** – pour les calculs de distances sur les points

```cypher
CREATE POINT INDEX … FOR (n:Personne) ON (n.coord)
```

### Plan d’exécution et options

- Plan d’exécution :
    - `EXPLAIN <query>` : <https://neo4j.com/docs/cypher-manual/current/execution-plans/>
    - Doit être exécuté dans Neo4j Desktop (ou online Sandbox)
- Options sur les requêtes :
    - `CYPHER <options> <query>`
    - Option possible : sélection d’un engin (« runtime ») : <https://neo4j.com/docs/cypher-manual/current/query-tuning/>

```cypher
EXPLAIN
CYPHER runtime = pipelined
MATCH (:Station {name: 'Denmark'})<-[:STOP]-(d:Str)
RETURN count(*)
```

## Modèles

Neo4j Graph Gists (<https://neo4j.com/graphgists/>)

Collection de graphes qui modélisent des données de différents domaines

- On peut exécuter les requêtes en ligne
- Voir les catégories en bas de page
- Attention, certaines sources de données ne sont plus disponibles

![](../images/lecons/10-1-graphes-optimisation-05-1.png)

## Exercice : utilisation d’index - base de données LNH

Pour une base de données de matchs de la Ligue nationale de hockey (LNH), étudiez un ensemble de requêtes et recommandez des index à utiliser

Voir l’exercice : [Graphes – Optimisation et index (LNH)](../exercices/Graphes_Optimisation_index_LNH.md)
