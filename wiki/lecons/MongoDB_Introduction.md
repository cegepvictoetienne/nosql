# Introduction à MongoDB

## MongoDB

- MongoDB est un SGBD orienté documents très utilisé en ce moment.
- Il est actuellement au top 5 des moteurs de bases de données, et la première place pour les SGBD NoSQL : 
    - <https://db-engines.com/en/ranking> (janvier 2026)
    - <https://db-engines.com/en/ranking_trend/system/MongoDB>
- La première version est sortie en 2009
- Mongo DB permet de manipuler des objets structurés au format BSON (JSON binaire)

## MongoDB – Installation locale

- Téléchargement et installation
    - <https://www.mongodb.com/try>
- Aide et documentation :
    - <https://docs.mongodb.com/manual/>
    - <https://docs.mongodb.com/manual/tutorial/>

## MongoDB Compass

MongoDBCompass est l’interface officielle pour MongoDB

![](../images/lecons/02-mongodb-intro-04-1.png)

## mongosh

**MongoDB Shell (`mongosh`)** est un outil ligne de commande (CLI) MongoDB permettant d’exécuter des commandes.

Il peut être utilisée pour manipuler les données et pour certaines opérations administratives.

L’interface est intégrée à *MongoDBCompass*. Elle est aussi disponible dans Devilbox dans le conteneur *mongodb*, et sous forme d’outil ligne de commande sous plusieurs systèmes d’exploitation, lien téléchargement:

[https://www.mongodb.com/docs/mongodb-shell/install/ ](https://www.mongodb.com/docs/mongodb-shell/install/)

### mongosh (suite)

`mongosh` est en fait l’interpréteur ligne de commande de NodeJS légèrement modifié:

- Javascript peut être utilisé
- Module d’accès à MongoDB rendu disponible automatiquement (`db.`)
- Commandes d’administration comme `use <bd>` et `show databases` ajoutées

Les scripts mongosh ont l’extension `.mongodb` ou `.mongodb.js`

## MongoDB for VS Code

Cette extension officielle de VS Code permet de:

- Se connecter à une base de données MongoDB
- D’explorer le contenu de la BD (db et collections)
- D’exécuter un script sous forme d’un fichier `.js` à l’aide d’une connexion à cette base de données.
- D’utiliser un IDE connu et profiter des autres extensions comme l’intégration git

![Extension MongoDB for VS Code](../images/lecons/02-mongodb-intro-07-2.png)

L’extension introduit une notion de *Playground* qui est un fichier `.mongodb.js` dont le segment sélectionné va être exécuté à l’aide d’une connexion MongoDB. L’entièreté du fichier va être exécuté si rien n’est sélectionné. Très utile pour peaufiner une séquence complexe de commandes.

!!! note

    L’aperçu des réponses dans la fenêtre à droite n’affiche pas l’ensemble des résultats

Un exemple de script est généré à la création d’un nouveau Playground.

!!! warning "Attention"

    L’utilisation des outils d’IA sera interdite pendant les examens. Je vous recommande de désactiver Github Copilot ou toute autre aide IA intégrée à votre VS Code pendant les exercices du cours.

## Database tools

Depuis la version 4.4, les outils connexes à Mongo DB sont offerts séparément de l’installateur Mongo. Ces outils permettent entre autres l’importation et l’exportation de bases de données.

Ces outils sont tout de même intégrés dans l’outil *MongoDB Compass*. Si vous préférez ne pas installer *MongoDBCompass* ou utiliser le mode console pour administrer vos bases de données, vous devez installer ces outils.

Téléchargement et installation : [https://www.mongodb.com/try/download/database-tools ](https://www.mongodb.com/try/download/database-tools)*(package msi recommandé)*

Le chemin vers ces les outils n’est pas ajouté automatiquement au %PATH% sur Windows

## MongoDB Atlas – service infonuagique

«Assurez des performances et une faible latence avec MongoDB Atlas Database grâce à une mise à l’échelle intuitive, des ajustements automatisés des ressources et une distribution mondiale des données. Des outils intégrés **optimisent les requêtes** et **éliminent les inefficacités**, tandis que les **mises à niveau sans interruption** maintiennent la vitesse et la fiabilité»

- Service infonuagique: version Entreprise de MongoDB maintenue par MongoDB sur ses serveurs
- Version de base disponible gratuitement <https://www.mongodb.com/cloud/atlas>
- Les *nodes* dans Atlas sont les instances de mongodb, elles sont regroupées en *clusters* (grappes)

![](../images/lecons/02-mongodb-intro-10-3.png)

### Accès réseau

- Pour se connecter au serveur on doit donner accès à notre adresse IP :

![](../images/lecons/02-mongodb-intro-11-4.png)

![](../images/lecons/02-mongodb-intro-11-5.png)

![](../images/lecons/02-mongodb-intro-11-6.png)

### Sécurité

L’accès à votre instance de base de données sur Atlas est sécurisé sur la base de l’adresse IP du client. Initialement, Atlas offre d’ajouter votre l’adresse IP à la liste des adresses permises, selon ce qu’il détecte par votre connexion à l’interface web.

Au CÉGEP, ce n’est pas suffisant: l’accès à l’Internet est fait via le réseau RISQ, qui est le réseau des institutions d’études supérieures au Québec, et le trafic circule en utilisant divers chemins ce qui fait que l’adresse IP vue par Atlas peut changer d’une connexion à l’autre.

*Project → Security → Database & Network Access → Network Access → IP Access List*

***206.167.16.0/22*** - RISQ (capture d’écran prochaine page)

En cas de problème, vous pouvez tester avec 0.0.0.0/0 (accès permis pour tous les IP) – mais ne le laisser pas à cette valeur!

![Liste d’accès IP dans Atlas](../images/lecons/02-mongodb-intro-13-7.png)

### Connexion

Pour se connecter, dans le GUI: *Clusters → Connect*

Choisir un type de connection, mais ce qui importe est le *Connection URI* (commence par *mongodb:* )

S’assurer d’avoir un utilisateur valide avec un mot de passe

![](../images/lecons/02-mongodb-intro-14-8.png)

![](../images/lecons/02-mongodb-intro-14-9.png)

## Exercice de connectivité

1. Connectez-vous à votre base de données locale (Devilbox)
    1. Via mongosh (exec dans le conteneur mongodb)
    1. À travers Compass puis le MongoDB Shell intégré
    1. À l’aide de l’extension VS Code pour MongoDB
1. Pour chaque connexion, insérer un document dans une nouvelle collection et faites afficher cette nouvelle collection dans les interfaces graphiques (Compass et VS Code)

**Suite :**

1. Créez-vous un compte sur Atlas et insérer un document dans une nouvelle collection via l’interface web du service infonuagique
1. Connectez-vous à la base de données Atlas (assurez-vous d’autoriser votre adresse IP)
    1. Via mongosh (exec dans le conteneur mongodb)
    1. À travers Compass puis le MongoDB Shell intégré
    1. À l’aide de l’extension VS Code pour MongoDB

## MongoDB – La syntaxe

!!! note

    Les termes en *italique* représentent les informations à ajuster selon le contexte d’utilisation.

### Commandes de base

| Commande | Description |
|---|---|
| `mongosh` | Lance l’interpréteur de commandes qui permet d’utiliser JavaScript. On peut y ajouter des [paramètres](https://docs.mongodb.com/manual/reference/connection-string/) pour se connecter à une BD distante (ex. MongoDB Atlas) |
| `use` *nom_de_la_bd* ([doc](https://www.mongodb.com/docs/mongodb-shell/run-commands/)) | Prévient le moteur de BD que les prochaines commandes concernent cette BD. **Si la base de données demandée n’existe pas, Mongo la crée automatiquement.** |

Exemple :

```javascript
use produits
```

### Insertion

```javascript
db.collection.insertOne(document)
db.collection.insertMany([documents])
```

- *collection* : nom de la collection de documents (analogue à une table en SQL)
- *document(s)* : valeur à insérer (objet ou tableau JavaScript) ([doc](https://www.mongodb.com/docs/mongodb-shell/crud/insert/#std-label-mongosh-insert))

**Insère** un ou plusieurs documents dans une collection de la base de données courante. **Si la collection n’existe pas, elle est créée.**

```javascript
db.produits.insertOne( {nom:"A", prix : 10.50, qte: 6} )
db.produits.insertOne( {nom:"C", prix : 100, qte: 5, categories : ["cat1", "cat2"] } )

const nouveaux_produits = [ {nom:"D", prix : 400, qte: 4},
                            {nom:"E", prix : 500, qte: 5} ];
db.produits.insertMany(nouveaux_produits);
```

### Recherche

```javascript
db.collection.find(req, proj)
```

- *req* : *Query*. Optionnel. Spécifie les critères de la recherche
- *proj* : *Projection*. Optionnel. Spécifie les champs du document à retourner
- [Documentation](https://www.mongodb.com/docs/mongodb-shell/crud/read/)

Sélectionne les documents correspondant à la recherche. Exemples :

```javascript
db.produits.find()  // tous les produits
db.produits.find( { nom : "A"})  // nom == 'A'
db.produits.find( { nom : "A"}, { nom : 1, prix : 1 })  // retourne nom et prix
db.produits.find( { prix: 100, qte: 9 } )  // prix 100 ET qte 9
db.produits.find( { prix:{ $gt:980 }, qte: 8 } )
```

### Mise à jour

```javascript
db.collection.updateOne(req, up)
db.collection.updateMany(req, up)
```

- *req* : Requête. Spécifie les critères de la recherche
    - Utiliser `{}` pour sélectionner tous les documents
    - (Mêmes sélecteurs que le `find`)
- *up* : *Update*. Opérations à effectuer sur les documents
- [Documentation](https://www.mongodb.com/docs/mongodb-shell/crud/update/#std-label-mongosh-update)

Met à jour les données correspondant à la sélection :

```javascript
db.produits.updateOne(
    { nom: "A"},
    { $set: { prix : 20.50 } }
) // Affecte seulement le premier document retourné par le filtre

db.produits.updateMany(
    { categorie: "légumes"},
    { $inc: { prix : 5 } }
)
```

### Suppression

```javascript
db.collection.deleteOne(req)
db.collection.deleteMany(req)
```

- *req* : Requête. Spécifie les critères de la recherche (mêmes sélecteurs que le `find`)
- [Documentation](https://www.mongodb.com/docs/mongodb-shell/crud/delete/#std-label-mongosh-delete)

Supprime les données correspondant à la sélection. Exemples :

```javascript
// Efface le premier selon le critère
db.produits.deleteOne({nom : "A"})
db.produits.deleteMany( { } ) // tous les documents
```

### Autres commandes

| Commande | Description |
|---|---|
| `db.collection.aggregate()` ([doc](https://www.mongodb.com/docs/mongodb-shell/run-agg-pipelines/)) | Permet d’effectuer des regroupements avec totaux ou des transformations *(nous reviendrons sur cette commande)* |
| `show databases` | Affiche la liste des bases de données du serveur |
| `show collections` | Affiche la liste des collections de la base de données en cours |
| Autres commandes | Documentation complète disponible sur le site de MongoDB : <https://www.mongodb.com/docs/manual/reference/method/js-collection/> |

## Exercice 2, section cinéma

Créez une base de données **cinema**. Effectuez les opérations demandées :

1. Ajoutez les 5 films suivants (*attention au **format** des données*) :

    | Titre | Date de sortie | Durée (min) | Acteurs principaux |
    |---|---|---|---|
    | Forrest Gump | 5 octobre 1984 | 140 minutes | Tom Hanks, Gary Sinise |
    | Tu ne tueras point | 9 novembre 2016 | 140 minutes | Mel Gibson |
    | La ligne verte | 1 mars 2000 | 189 minutes | Tom Hanks, Michael Clark Duncan |
    | Your name | 28 décembre 2016 |  | Ryûnosuke Kamiki, Mone Kamishiraishi |
    | Django Unchained |  | 164 minutes | Jamie Foxx, Christoph Waltz |

2. Trouvez la requête permettant d'obtenir :
    - La liste de tous les films
    - Les films sortis en 2016
    - Les films de plus de 150 minutes
    - Les films dans lesquels Tom Hanks a joué
    - Les films ayant un seul acteur principal
3. Mettez à jour l’information d’un film : le film « Your name » a une durée de 106 min.
4. Supprimez tous les films

## Sélecteurs de requêtes

<https://www.mongodb.com/docs/manual/reference/mql/query-predicates/>

Opérateurs ciblés dans le cadre du cours Mégadonnées :

- Opérateurs de comparaison (`$eq`, `$gt`, `$gte`, `$in`, `$lt`, `$lte`, `$ne`, `$nin`)
- Opérateurs logiques (`$and`, `$or`)
- Opérateurs d'éléments (`$exists`, `$type`)
- Opérateurs de tableaux (`$all`, `$elemMatch`, `$size`)

## MongoDB – Modélisation

**Modèle flexible** : les documents d’une même collection peuvent avoir des champs différents

```javascript
db.contacts.find()
[ {nom: "jean", age: "55"},
  {nom: "samuel", num_telephone: "819-555-4536"} ]
```

**Comment modéliser les relations** ([doc](https://docs.mongodb.com/manual/applications/data-models-relationships/)) :

- Relation avec documents imbriqués
- Relation avec références

Relation 1 à 1 avec un document imbriqué :

![Relation 1 à 1 avec un document imbriqué](../images/lecons/02-mongodb-intro-27-10.png)

Relation avec référence à un document :

![Relation avec référence à un document](../images/lecons/02-mongodb-intro-28-11.png)

## Importation (Database tools)

Pour importer un fichier JSON sur un serveur : commande `mongoimport` (<https://www.mongodb.com/compatibility/json-to-mongodb>)

**Commande de base :**

```bash
mongoimport --db nomBD --collection nomCollection --drop --file cheminAcces/nomFichier.json
```

!!! tip

    Le paramètre `--jsonArray` doit être ajouté lorsque les données sont organisées sous forme de tableau.

**Commande pour importation sur un serveur distant :**

```bash
mongoimport --uri mongodb+srv://username:pass@cluster0-???.mongodb.net/dbEvaluationPointsInterets --collection restaurants --drop --file primer-dataset.json
```

`mongoimport.exe` est disponible dans le dossier de programmes utilisé pour l’installation Mongo.
Ex. : `C:\Program Files\MongoDB\Tools\100\bin`

## Importation de collections

1. Téléchargez les 3 collections mises à votre disposition
    - `persons.json`
    - `restaurants.json`
    - `grades.json`
2. Importez les 3 collections à partir de l’outil MongoDB Compass ou de la commande présentée à la section précédente.
3. Prenez le temps d’analyser la structure de données de chacun des modèles proposés.
4. Rédigez les requêtes pour obtenir les réponses aux questions des sections suivantes

Sources :

- <https://docs.atlas.mongodb.com/sample-data/available-sample-datasets/>
- <https://docs.atlas.mongodb.com/sample-data/sample-restaurants/>
- <https://json-generator.com/>

## Restaurants

Exemple :

![](../images/lecons/02-mongodb-intro-31-12.png)

Requêtes :

- Liste des restaurants de type (cuisine) “Chinese”
- Liste des restaurants dont le code postal est “10003”
- Liste des restaurants de type (cuisine) “French” dans le Queens (borough)
- Liste des restaurants à Manhattan ou Brooklyn (borough)
- Liste des restaurants de type (cuisine) “Chicken” à Manhattan ou Brooklyn
- Liste des restaurants ayant reçu un score supérieur à 70
- Liste des restaurants ayant reçu un score entre 90 et 100
- Liste des restaurants qui ne sont pas à Manhattan

## Persons

Exemple :

![](../images/lecons/02-mongodb-intro-33-13.png)

Requêtes :

- Liste des personnes actives
- Liste des personnes ayant les yeux verts
- Liste des personnes de plus de 18 ans
- Liste des personnes ayant **exactement** 3 amis (*<https://docs.mongodb.com/manual/tutorial/query-arrays/>*)
- **Défi** (*facultatif, à réaliser* ***après*** *avoir terminé les autres requêtes*) : Liste des personnes ayant une balance entre 5 000$ et 10 000$ *(Vous devez d’abord convertir la balance en nombre)*

## Grades

Exemple :

![](../images/lecons/02-mongodb-intro-35-14.png)

Requêtes :

- Liste des scores au quiz
- Liste des scores de l’étudiant #1 (`student_id: 1`)
- Liste des scores inférieurs à 60 à l’examen

## En devoir

- Complétez les requêtes non terminées
