# Graphes – Optimisation et index (LNH)

**Thème :** classement des équipes de la LNH (division Atlantique 2025-26)

Ligue nationale de hockey (LNH) : matchs entre équipes de la division Atlantique, saison 2025-26.

## Modèle de données

**Nœuds :**

```cypher
(:Team  { id, nickname, slug })
(:Game  { id, attendance, year, month, day })
```

**Relations :**

```cypher
(:Team)-[:HOME_TEAM { goals, outcome, win, points }]->(:Game)
(:Team)-[:AWAY_TEAM { goals, outcome, win, points }]->(:Game)
```

- `outcome` : `'win'`, `'loss'`, `'overtime_loss'`
- `win` : 1 si victoire, 0 sinon
- `points` : 2 (victoire), 1 (défaite en prolongation), 0 (défaite)

Schéma simplifié :

```cypher
(Bruins)-[:HOME_TEAM {goals:3, outcome:'win', win:1, points:2}]->(Game#42)
(Canadiens)-[:AWAY_TEAM {goals:2, outcome:'loss', win:0, points:0}]->(Game#42)
```

## Partie 1 – Mise en place de la base de données

Exécutez ces requêtes dans Neo4j Browser dans l'ordre indiqué.

### Étape 1 : Contraintes d'unicité

```cypher
CREATE CONSTRAINT FOR (n:Team) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT FOR (n:Game) REQUIRE n.id IS UNIQUE;
```

### Étape 2 : Création des équipes

```cypher
CREATE
  (:Team {id:'team-buf', nickname:'Sabres',      slug:'nhl-buf-sabres'}),
  (:Team {id:'team-tbl', nickname:'Lightning',   slug:'nhl-tbl-lightning'}),
  (:Team {id:'team-mtl', nickname:'Canadiens',   slug:'nhl-mtl-canadiens'}),
  (:Team {id:'team-bos', nickname:'Bruins',      slug:'nhl-bos-bruins'}),
  (:Team {id:'team-ott', nickname:'Senators',    slug:'nhl-ott-senators'}),
  (:Team {id:'team-det', nickname:'Red Wings',   slug:'nhl-det-red-wings'}),
  (:Team {id:'team-tor', nickname:'Maple Leafs', slug:'nhl-tor-maple-leafs'}),
  (:Team {id:'team-fla', nickname:'Panthers',    slug:'nhl-fla-panthers'});
```

### Étape 3 : Création des matchs et relations `HOME_TEAM` / `AWAY_TEAM`

??? abstract "Requête de création des 30 matchs"

    ```cypher
    WITH [
      {id:'g01', home:'team-bos', away:'team-buf', hg:4, ag:2, ot:false, year:2025, month:10, day:10, att:17565},
      {id:'g02', home:'team-tbl', away:'team-mtl', hg:3, ag:1, ot:false, year:2025, month:10, day:11, att:19092},
      {id:'g03', home:'team-ott', away:'team-det', hg:3, ag:2, ot:true,  year:2025, month:10, day:14, att:18652},
      {id:'g04', home:'team-tor', away:'team-fla', hg:1, ag:4, ot:false, year:2025, month:10, day:16, att:18819},
      {id:'g05', home:'team-buf', away:'team-mtl', hg:3, ag:0, ot:false, year:2025, month:10, day:18, att:16325},
      {id:'g06', home:'team-det', away:'team-bos', hg:2, ag:3, ot:true,  year:2025, month:10, day:21, att:19515},
      {id:'g07', home:'team-fla', away:'team-tbl', hg:2, ag:5, ot:false, year:2025, month:10, day:23, att:17921},
      {id:'g08', home:'team-mtl', away:'team-ott', hg:4, ag:3, ot:false, year:2025, month:10, day:25, att:21105},
      {id:'g09', home:'team-bos', away:'team-tor', hg:2, ag:1, ot:false, year:2025, month:10, day:28, att:17565},
      {id:'g10', home:'team-buf', away:'team-det', hg:5, ag:3, ot:false, year:2025, month:10, day:30, att:16402},
      {id:'g11', home:'team-tbl', away:'team-ott', hg:3, ag:2, ot:true,  year:2025, month:11, day:1,  att:19201},
      {id:'g12', home:'team-fla', away:'team-mtl', hg:1, ag:3, ot:false, year:2025, month:11, day:4,  att:17654},
      {id:'g13', home:'team-det', away:'team-tor', hg:4, ag:2, ot:false, year:2025, month:11, day:6,  att:19515},
      {id:'g14', home:'team-ott', away:'team-buf', hg:3, ag:4, ot:false, year:2025, month:11, day:8,  att:18321},
      {id:'g15', home:'team-mtl', away:'team-tbl', hg:2, ag:4, ot:false, year:2025, month:11, day:11, att:21302},
      {id:'g16', home:'team-tor', away:'team-bos', hg:0, ag:3, ot:false, year:2025, month:11, day:13, att:18950},
      {id:'g17', home:'team-fla', away:'team-det', hg:3, ag:2, ot:false, year:2025, month:11, day:15, att:17812},
      {id:'g18', home:'team-buf', away:'team-tbl', hg:1, ag:2, ot:false, year:2025, month:11, day:18, att:16789},
      {id:'g19', home:'team-ott', away:'team-mtl', hg:2, ag:1, ot:false, year:2025, month:11, day:20, att:18654},
      {id:'g20', home:'team-bos', away:'team-fla', hg:4, ag:3, ot:true,  year:2025, month:11, day:22, att:17565},
      {id:'g21', home:'team-det', away:'team-buf', hg:1, ag:2, ot:false, year:2025, month:12, day:2,  att:19515},
      {id:'g22', home:'team-tor', away:'team-ott', hg:3, ag:2, ot:false, year:2025, month:12, day:4,  att:18945},
      {id:'g23', home:'team-mtl', away:'team-bos', hg:2, ag:4, ot:false, year:2025, month:12, day:6,  att:21207},
      {id:'g24', home:'team-tbl', away:'team-det', hg:3, ag:1, ot:false, year:2025, month:12, day:9,  att:19002},
      {id:'g25', home:'team-fla', away:'team-ott', hg:4, ag:1, ot:false, year:2025, month:12, day:11, att:17543},
      {id:'g26', home:'team-buf', away:'team-tor', hg:3, ag:2, ot:true,  year:2025, month:12, day:13, att:16851},
      {id:'g27', home:'team-bos', away:'team-mtl', hg:3, ag:2, ot:true,  year:2025, month:12, day:16, att:17565},
      {id:'g28', home:'team-det', away:'team-fla', hg:3, ag:2, ot:false, year:2025, month:12, day:18, att:19515},
      {id:'g29', home:'team-ott', away:'team-tor', hg:4, ag:3, ot:false, year:2025, month:12, day:20, att:18710},
      {id:'g30', home:'team-tbl', away:'team-buf', hg:3, ag:2, ot:false, year:2025, month:12, day:23, att:19128}
    ] AS matchs
    UNWIND matchs AS m
    CREATE (g:Game {id:m.id, year:m.year, month:m.month, day:m.day, attendance:m.att})
    WITH m, g
    MATCH (h:Team {id: m.home})
    CREATE (h)-[:HOME_TEAM {
      goals:   m.hg,
      outcome: CASE WHEN m.hg > m.ag THEN 'win'
                    WHEN m.hg < m.ag THEN 'loss'
                    ELSE CASE WHEN m.ot THEN 'overtime_loss' ELSE 'draw' END END,
      win:     CASE WHEN m.hg > m.ag THEN 1 ELSE 0 END,
      points:  CASE WHEN m.hg > m.ag THEN 2
                    WHEN m.hg < m.ag THEN 0
                    WHEN m.ot        THEN 1 ELSE 0 END
    }]->(g)
    WITH m, g
    MATCH (a:Team {id: m.away})
    CREATE (a)-[:AWAY_TEAM {
      goals:   m.ag,
      outcome: CASE WHEN m.ag > m.hg THEN 'win'
                    WHEN m.ag < m.hg THEN 'loss'
                    ELSE CASE WHEN m.ot THEN 'overtime_loss' ELSE 'draw' END END,
      win:     CASE WHEN m.ag > m.hg THEN 1 ELSE 0 END,
      points:  CASE WHEN m.ag > m.hg THEN 2
                    WHEN m.ag < m.hg THEN 0
                    WHEN m.ot        THEN 1 ELSE 0 END
    }]->(g);
    ```

### Vérification

```cypher
MATCH (n)
RETURN labels(n) AS `Type de nœud`, count(*) AS total;
```

Résultat attendu : 8 équipes et 30 matchs.

## Partie 2 – Requêtes typiques de l'application

### Requête A – Compter les nœuds par type

```cypher
MATCH (n)
RETURN labels(n) AS `Type de nœud`, count(*) AS total
```

### Requête B – Afficher les matchs d'une équipe spécifique (les Bruins)

```cypher
MATCH (t1:Team {nickname: 'Bruins'})-[r1]->(g1)<-[r2]-(t2)
RETURN t1, r1, g1, r2, t2
```

### Requête C – Calculer le pourcentage de victoires de chaque équipe

```cypher
MATCH (n:Team)-[r]->(g:Game)
WITH n.nickname AS equipe, sum(r.win) AS victoires, count(r) AS matchs
RETURN equipe, victoires, matchs, (victoires * 1.0 / matchs * 1.0) AS pct_victoires
```

### Requête D – Répartition des matchs à domicile et à l'extérieur par équipe

```cypher
MATCH (t:Team)-[r]->(x:Game)
WITH t.nickname AS equipe,
     CASE TYPE(r) WHEN 'AWAY_TEAM' THEN 1 ELSE 0 END AS match_ext,
     CASE TYPE(r) WHEN 'HOME_TEAM' THEN 1 ELSE 0 END AS match_dom,
     r
RETURN equipe,
       sum(match_ext) AS matchs_exterieur,
       sum(match_dom) AS matchs_domicile,
       count(r)       AS total_matchs
ORDER BY total_matchs DESC
```

### Requête E – Différentiel de buts par équipe

```cypher
MATCH (t1:Team)-[r1]->(g1:Game)<-[r2]-(adversaire:Team)
WITH t1.nickname AS equipe, sum(r1.goals) AS buts_pour, sum(r2.goals) AS buts_contre
RETURN equipe, buts_pour, buts_contre, buts_pour - buts_contre AS differentiel
ORDER BY differentiel DESC
```

### Requête F – Retrouver une équipe par son identifiant unique (slug)

```cypher
MATCH (t:Team {slug: 'nhl-mtl-canadiens'})
RETURN t
```

### Requête G – Retrouver les matchs d'un mois précis (novembre 2025)

```cypher
MATCH (g:Game)
WHERE g.year = 2025 AND g.month = 11
RETURN g
ORDER BY g.day
```

### Requête H – Trouver les équipes dont le surnom contient 'ings'

```cypher
MATCH (t:Team)
WHERE t.nickname CONTAINS 'ings'
RETURN t.nickname
```

### Requête I – Trouver les équipes dont le slug commence par 'nhl-mtl'

```cypher
MATCH (t:Team)
WHERE t.slug STARTS WITH 'nhl-mtl'
RETURN t
```

## Partie 3 – Questions

**Q1.** Pour chacune des requêtes A à I, identifiez :

1. Quelle(s) propriété(s) de nœud sont utilisées comme critère de filtrage (dans `WHERE` ou `{…}`) ?
2. Quel type d'index serait le plus approprié ? (`RANGE` / `TEXT` / aucun index utile)
3. Rédigez la commande `CREATE INDEX` correspondante, si applicable.

**Q2.** Les propriétés `outcome`, `win` et `points` se trouvent sur les **relations** `HOME_TEAM` et `AWAY_TEAM` (pas sur les nœuds). Dans les requêtes C et D, ces propriétés sont utilisées via `sum(r.win)` et `TYPE(r)`.

1. Peut-on créer un index sur une propriété de relation dans Neo4j ?
2. Quelle modification du modèle de données permettrait d'indexer ces valeurs si elles étaient très souvent filtrées ?

**Q3.** Comparez les requêtes H (`CONTAINS`) et I (`STARTS WITH`) sur `Team.slug` / `Team.nickname`. Si vous ne pouvez créer qu'un seul index sur `Team.nickname`, lequel choisissez-vous : `RANGE` ou `TEXT` ? Justifiez.

**Q4.** Utilisez `EXPLAIN` sur la requête B avant et après avoir créé votre index.

1. Quel opérateur apparaît avant l'index ? (ex. : `NodeByLabelScan`)
2. Quel opérateur le remplace après la création de l'index ?

Syntaxe :

```cypher
EXPLAIN
MATCH (t1:Team {nickname: 'Bruins'})-[r1]->(g1)<-[r2]-(t2)
RETURN t1, r1, g1, r2, t2
```
