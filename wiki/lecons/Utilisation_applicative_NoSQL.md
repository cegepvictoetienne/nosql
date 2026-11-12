# Utilisation applicative des systèmes de bases de données NoSQL

## ODM pour MongoDB

- **Qu'est-ce qu'un ODM?**
    - **Object Document Mapper**
    - Couche d'abstraction entre l'application et la base de données MongoDB
    - Permet de modéliser des documents comme des objets JavaScript (classes/schémas)
    - Offre : validation, typage, valeurs par défaut, relations, middlewares
    - Similaire à un ORM (Object-Relational Mapper) pour les bases de données relationnelles

- **Avec ODM :**
    - Code structuré avec schémas définis explicitement
    - Validation automatique des données avant l'écriture en base
    - Méthodes pratiques intégrées : `findById()`, `create()`, `save()`, `populate()`…
    - Gestion simplifiée des relations entre collections
- **Sans ODM :**
    - On travaille directement avec les méthodes de bas niveau du driver officiel MongoDB
    - Aucune abstraction des relations
    - Plus de code répétitif, plus de risques d'incohérence des données

## Mongoose

- **Mongoose** est la bibliothèque ODM la plus populaire pour MongoDB avec Node.js
- **Caractéristiques :**
    - Définition de schémas typés (String, Number, Date, Array, ObjectId…)
    - Validation automatique avant l'écriture en base
    - Middlewares (hooks) : pre/post save, find, delete…
    - Population : résolution de références entre collections
    - Méthodes et propriétés virtuelles sur les modèles
- Référence : <https://mongoosejs.com>
- Installation : `npm install mongoose`

## Mongoose – Connexion

- **Connexion à MongoDB avec Mongoose :**

```javascript
import mongoose from 'mongoose';

async function connecter() {
  try {
    await mongoose.connect('mongodb://localhost:27017/maBaseDeDonnees');
    console.log('Connexion réussie');
  } catch (err) {
    console.error('Erreur :', err);
  }
}

// L'URI peut pointer vers MongoDB Atlas (infonuagique) ou un serveur local
```

## Mongoose – Schéma et modèle

- Un **schéma** définit la structure des documents d'une collection.
- Un **modèle** est une classe JavaScript construite à partir d'un schéma.

```javascript
import { Schema, model } from 'mongoose';

const produitSchema = new Schema({
  nom:      { type: String, required: true },
  prix:     { type: Number, min: 0 },
  quantite: { type: Number, default: 0 },
  categories: [String],
  createdAt:{ type: Date, default: Date.now }
});

// Créer un modèle à partir du schéma :
const Produit = model('Produit', produitSchema);
```

## Mongoose – Création

- **Création de documents :**

```javascript
// Méthode 1 : Model.create()
const nouveauProduit = await Produit.create({
  nom: 'Laptop',
  prix: 999.99,  quantite: 5,
  categories: ['electronique', 'informatique']
});

// Méthode 2 : instanciation + save()
const p = new Produit({ nom: 'Souris', prix: 29.99 });
await p.save();

// Mongoose valide automatiquement les données selon le schéma avant l'insertion
```

## Mongoose – Lecture

- **Lecture de documents :**

```javascript
// Tous les documents
const produits = await Produit.find();

// Avec filtre (même syntaxe que MongoDB)
const chers = await Produit.find({ prix: { $gt: 500 } });

// Par identifiant MongoDB (_id)
const p = await Produit.findById(id);

// Premier résultat correspondant
const laptop = await Produit.findOne({ nom: 'Laptop' });

// Tri, projection, limite (chaînable)
const top5 = await Produit.find({})
  .sort({ prix: -1 }).limit(5).select('nom prix');
```

## Mongoose – Mise à jour et suppression

```javascript
// Mise à jour – retourne le document mis à jour
await Produit.findByIdAndUpdate(id,
  { $set: { prix: 899.99 } },
  { new: true }
);

// Mise à jour de plusieurs documents
await Produit.updateMany({ categorie: 'electronique' }, { $inc: { prix: 10 } });

// Suppression – supprimer un document par _id
await Produit.findByIdAndDelete(id);

// Suppression – supprimer selon un critère
await Produit.deleteMany({ quantite: 0 });
```

## Mongoose – Population (références)

- La **population** (`populate()`) permet de résoudre les références entre collections (comme un JOIN en SQL).

```javascript
// Définition du schéma avec référence :
const commandeSchema = new Schema({
  client: { type: Schema.Types.ObjectId, ref: 'Client' },
  produits: [{ type: Schema.Types.ObjectId, ref: 'Produit' }]
});

// Requête avec population automatique des références :
const commande = await Commande.findById(id)
  .populate('client')
  .populate('produits');

// commande.client et commande.produits contiennent les documents complets
```

## OGM pour Neo4j

- **Qu'est-ce qu'un OGM?**
    - **Object Graph Mapper**
    - Couche d'abstraction entre l'application et la base de données de graphes
    - Permet de modéliser des nœuds et des relations comme des objets JavaScript
    - Offre : schémas de nœuds, validation, gestion des relations, requêtes simplifiées
    - Similaire à un ODM, mais pour les graphes (nœuds + relations)

- **Avec OGM :**
    - Code structuré avec modèles de nœuds définis explicitement
    - Validation automatique des propriétés des nœuds
    - Méthodes pratiques : `create()`, `find()`, `first()`, `relateTo()`, `get()`…
    - Gestion déclarative des relations entre modèles
- **Sans OGM :**
    - On exécute directement des requêtes Cypher via le driver officiel Neo4j
    - Aucune abstraction des nœuds/relations, pas de validation de schéma
    - Plus de code Cypher manuel, plus de risques d'incohérence du graphe

## Neode

- **Neode** est un OGM pour Neo4j développé pour Node.js
- **Caractéristiques :**
    - Définition de modèles (nœuds) avec types et contraintes
    - Validation automatique des propriétés
    - Abstraction des opérations CRUD sur les nœuds
    - Gestion déclarative des relations entre modèles
    - Possibilité d'exécuter des requêtes Cypher personnalisées si nécessaire
- Référence : <https://github.com/adam-cowley/neode>
- Installation : `npm install neode`

## Neode – Connexion

- **Connexion à Neo4j avec Neode :**

```javascript
import Neode from 'neode';

const instance = new Neode(
  'bolt://localhost:7687',
  'neo4j',            // utilisateur
  'motdepasse'         // mot de passe
);

// Ou en utilisant des variables d'environnement (.env) :
const instance = new Neode(
  process.env.NEO4J_PROTOCOL + '://' + process.env.NEO4J_HOST,
  process.env.NEO4J_USERNAME,
  process.env.NEO4J_PASSWORD
);

// Le protocole bolt:// est le protocole binaire natif de Neo4j (performances optimales)
```

## Neode – Définir un modèle

- Un **modèle Neode** correspond à un label de nœud dans Neo4j.

```javascript
instance.model('Personne', {
  id:  { type: 'uuid', primary: true },
  nom: { type: 'string', required: true },
  age: { type: 'integer', default: 0 },
  actif: { type: 'boolean', default: true },
  // Relation déclarée dans le modèle
  amis: {
    type: 'relationships',
    relationship: 'CONNAIT',
    target: 'Personne',
    direction: 'out'
  }
});
```

## Neode – Création et lecture

```javascript
// Création :
const alice = await instance.create('Personne', {
  nom: 'Alice', age: 30
});
// alice est un objet Neode Node avec les propriétés du nœud créé

// Lecture – par clé primaire (uuid) :
const noeud = await instance.find('Personne', uuid);

// Premier résultat par propriété :
const p = await instance.first('Personne', 'nom', 'Alice');

// Tous les nœuds d'un modèle :
const tous = await instance.all('Personne');
```

## Neode – Mise à jour et suppression

```javascript
// Mise à jour – propriétés d'un nœud (sur l'objet Neode Node) :
const p = await instance.first('Personne', 'nom', 'Alice');
await p.update({ age: 31 });

// Suppression – supprimer un nœud :
await p.delete();

// Suppression avec toutes ses relations (detach delete) :
await p.detach();

// Requête Cypher personnalisée (si nécessaire) :
const res = await instance.cypher(
  'MATCH (p:Personne) WHERE p.age > $min RETURN p',
  { min: 18 }
);
```

## Neode – Relations

- Les **relations** déclarées dans le modèle peuvent être manipulées directement :

```javascript
// Créer une relation entre deux nœuds :
const alice = await instance.first('Personne', 'nom', 'Alice');
const bob   = await instance.first('Personne', 'nom', 'Bob');

// alice -[:CONNAIT]-> bob
await alice.relateTo(bob, 'amis');

// Récupérer les nœuds liés :
const amis = await alice.get('amis');
amis.forEach(a => console.log(a.get('nom')));

// Les propriétés d'un nœud se lisent avec .get('propriete')
```

## Comparaison ODM / OGM

| Critère | Mongoose (ODM) | Neode (OGM) |
|---|---|---|
| Base de données | MongoDB (documents) | Neo4j (graphes) |
| Unité de base | Document JSON/BSON | Nœud + Relation |
| Modélisation | Schéma + Modèle | Modèle (label) |
| Langage de requête | Méthodes + MQL | Méthodes + Cypher |
| Relations | Population (ref) | `relateTo()` / `get()` |
| Validation | Intégrée au schéma | Intégrée au modèle |
| Hooks / Middleware | Oui (pre/post save…) | Non (natif) |

*Dans les deux cas : le pattern ODM/OGM simplifie le code applicatif et améliore la maintenabilité*
