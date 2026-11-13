# MongoDB – La syntaxe

!!! note

    Les termes en *italique* représentent les informations à ajuster selon le contexte d’utilisation.

## Commandes de base

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

## Exercice 1, section cinéma

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

## Sélecteurs d'éléments  

<https://www.mongodb.com/docs/manual/reference/mql/query-predicates/>

Opérateurs ciblés dans le cadre du cours Mégadonnées :

- Opérateurs de comparaison (`$eq`, `$gt`, `$gte`, `$in`, `$lt`, `$lte`, `$ne`, `$nin`)
- Opérateurs logiques (`$and`, `$or`)
- Opérateurs d'éléments (`$exists`, `$type`)
- Opérateurs de tableaux (`$all`, `$elemMatch`, `$size`)  



# MongoDB – Modélisation

**Modèle flexible** : les documents d’une même collection peuvent avoir des champs différents

```javascript
db.contacts.find()
[ {nom: "jean", age: "55"},
  {nom: "samuel", num_telephone: "819-555-4536"} ]
```

**Comment modéliser les relations** ([doc](https://docs.mongodb.com/manual/applications/data-models-relationships/)) :

- Relation avec documents imbriqués
- Relation avec références

```json title="Relation 1 à 1 avec un document imbriqué"
 {
    id: "joe",
    name: "Joe Bookreader",
    address: {
        street: "123 Fake Street"
        city: "Faketon",
        state: "MA",
        zip: "12345"
    }
}

```

```json title="Relation avec référence à un document"
 Collection: publishers
 {
    id: "la_pasteque",
    name: "Édition La Pastèque",
    location: "Montreal"
 }

 Collection: books
 {
    title: "Paul à Québec",
    language: "Fr",
    publisher_id: "la_pasteque"
 }
```

# Importation (Database tools)

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
    - [people.json](../donnees/people.json)  
    - [restaurants.json](../donnees/restaurants.json)  
    - [grades.json](../donnees/grades.json)  
2. Importez les 3 collections à partir de l’outil MongoDB Compass ou de la commande présentée à la section précédente.
3. Prenez le temps d’analyser la structure de données de chacun des modèles proposés.
4. Rédigez les requêtes pour obtenir les réponses aux questions des sections suivantes

Sources :

- <https://docs.atlas.mongodb.com/sample-data/available-sample-datasets/>
- <https://docs.atlas.mongodb.com/sample-data/sample-restaurants/>
- <https://json-generator.com/>

## Restaurants

Exemple :

```json 
{
    "_id" : ObjectId("5c5ddad9d881c43d4c81c861"),
    "address": {
        "building" : "2780",
        "coord" : [
            -73.98241999999999,
            40.579505
        ],
        "street": "Stilwell Avenue",
        "zipcode": "11224"
    },
    "borough" : "Brooklyn",
    "cuisine" : "American",
    "grades" : [
        {
            "date" : ISODate("2014-06-10T00:00:00z"),
            "grade" : "A",
            "score" : 5
        }.
        {
            "date" : ISODate("2013-06-0500:00:00z"),
            "grade" : "A",
            "score" : 7
        },
        {
            "date" : ISODate("2012-04-13T00:00:00z"),
            "grade" : "A",
            "score" : 12
        }.
        {
            "date" : ISODate("2011-10-1200:00:00z"),
            "grade" : "A",
            "score" : 12
        }
    ],
    "name" : "Riviera Caterer",
    "restaurant_id" : "40356018"
}

```

Requêtes :

- Liste des restaurants de type (cuisine) “Chinese”
- Liste des restaurants dont le code postal est “10003”
- Liste des restaurants de type (cuisine) “French” dans le Queens (borough)
- Liste des restaurants à Manhattan ou Brooklyn (borough)
- Liste des restaurants de type (cuisine) “Chicken” à Manhattan ou Brooklyn
- Liste des restaurants ayant reçu un score supérieur à 70
- Liste des restaurants ayant reçu un score entre 90 et 100
- Liste des restaurants qui ne sont pas à Manhattan

## People

Exemple :

```json  
{
    "_id": "5c5dd07a4d06e5f1614b4231",
    "isActive": false,
    "balance": "$3,723.17",
    "picture": "http://placehold.it/32x32",
    "age": 36,
    "eyeColor": "green",
    "name": { "first": "Dale", "last": "Schultz" },
    "company": "EARTHPURE",
    "email": "dale.schultz@earthpure.tv",
    "phone": "+1 (924) 473-2869",
    "address": "497 Bay Street, Frank, South Carolina, 9747",
    "about": "Officia consectetur quis non elit. Cillum do minim cupidatat aliquip occaident est culpa sint commodo dolor officia commodo. Ut mollit veniam sunt fugiat molrud Lorem commodo do non culpa. Lorem nostrud excepteur fugiat aliqua.",
    "registered": "Wednesday, October 18, 2017 5:19 PM",
    "latitude": "-75.290003",
    "longitude": "-76.192721",
    "tags": ["fugiat", "duis", "anim", "Lorem", "nulla"],
    "friends": [
      { "name": "Henry Boyer" },
      { "name": "Jaclyn Montgomery" }
    ],
    "greeting": "Hello, Dale! You have 8 unread messages.",
    "favoriteFruit": "banana"
  },
```

Requêtes :

- Liste des personnes actives
- Liste des personnes ayant les yeux verts
- Liste des personnes de plus de 18 ans
- Liste des personnes ayant **exactement** 3 amis (*<https://docs.mongodb.com/manual/tutorial/query-arrays/>*)
- **Défi** (*facultatif, à réaliser* ***après*** *avoir terminé les autres requêtes*) : Liste des personnes ayant une balance entre 5 000$ et 10 000$ *(Vous devez d’abord convertir la balance en nombre)*

## Grades

Exemple :

```json 
  { "_id": { "$oid": "5c5ddba3d881c43d4c82c126" }, "student_id": 0, "type": "quiz", "score": 31.95004496742112 },
  { "_id": { "$oid": "5c5ddba3d881c43d4c82c127" }, "student_id": 1, "type": "homework", "score": 44.31667452616328 },
  { "_id": { "$oid": "5c5ddba3d881c43d4c82c128" }, "student_id": 0, "type": "exam", "score": 54.6535436362647 },
```

Requêtes :

- Liste des scores au quiz
- Liste des scores de l’étudiant #1 (`student_id: 1`)
- Liste des scores inférieurs à 60 à l’examen

## En devoir

- Complétez les requêtes non terminées
