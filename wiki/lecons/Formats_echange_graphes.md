# Formats d'échange de graphes

## Plan

- Introduction
- GraphML
- JSON-LD
- Comparaison (GraphML vs JSON-LD)
- Utilisation avec Neo4j (APOC)
- Outils et ressources (json-ld.org)

## Introduction

- Le besoin d'échange de données de graphes est croissant.
- Interopérabilité entre différents systèmes (Neo4j, Memgraph, ArangoDB, etc.)
- Partage de jeux de données (Datasets) standardisés.
- Sémantique commune pour SEO/IA

## Bases de données de graphes populaires

- Neo4j : Leader du marché, utilise le langage Cypher.
- Memgraph : Base de données 'In-Memory' ultra-rapide pour le temps réel.
- ArangoDB : Multi-modèle (Graphes + Documents), très flexible.

## GraphML

- Basé sur XML (eXtensible Markup Language).
- Standard ouvert et robuste pour l'échange de graphes.
- Supporte les attributs personnalisés pour les nœuds et les relations.
- Structure hiérarchique complète : `<graph>`, `<node>`, `<edge>`.

**Exemple GraphML (XML)**

```xml
<graphml xmlns="http://graphml.graphdrawing.org/xmlns">
  <graph id="G" edgedefault="directed">
    <node id="n0"/>
    <node id="n1"/>
    <edge id="e0" source="n0" target="n1"/>
  </graph>
</graphml>
```

## JSON-LD

- Basé sur JSON (JSON for Linked Data).
- Standard W3C pour l'interopérabilité des données sur le Web.
- Mise en œuvre du concept RDF (Resource Description Framework)
- Utilise un `@context` pour définir la sémantique des propriétés.
- Permet de lier des données à travers différents serveurs (Linked Data).
- Un URI représente une entité – JSON-LD décrit cette entité avec un vocabulaire connu (*schema.org*) et ses liens avec d’autres entités via des URIs.

**Exemple JSON-LD (Sémantique)**

```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "Étienne Rivard",
  "jobTitle": "Professor",
  "worksFor": {
    "@type": "Organization",
    "name": "Cégep de Victoriaville"
  },
  "colleague": [
    "http://www.cegepvicto.ca/SebastienTrottier.jsonld",
    "http://www.cegepvicto.ca/SebastienTrottier.jsonld"
  ]
}
```

## Autre exemple JSON-LD (Produit Shopify/SEO)

```json
{
  "@context": "https://schema.org/",
  "@type": "Product",
  "name": "T-Shirt Mégadonnées",
  "description": "T-shirt confortable pour experts NoSQL.",
  "brand": {
    "@type": "Brand",
    "name": "Cégep de Victoriaville"
  },
  "offers": {
    "@type": "Offer",
    "priceCurrency": "CAD",
    "price": "29.99",
    "availability": "https://schema.org/InStock"
  }
}
```

## Outils et ressources (json-ld.org)

- Site officiel : <https://json-ld.org/>
- Bac à sable JSON-LD pour tester et visualiser les données.
- Documentation complète des spécifications W3C.
- Outils de conversion et validateurs en ligne.

## Comparaison (GraphML vs JSON-LD)

| Caractéristique | GraphML | JSON-LD |
|---|---|---|
| Format de base | XML | JSON |
| Interopérabilité | Logiciels de graphes (Gephi) | Web sémantique / W3C |
| Complexité | Plus rigide | Flexible (via `@context`) |
| Usage type | Analyse de graphes pure | Données liées / SEO / Knowledge Graphs |

## Utilisation avec Neo4j (APOC & neosemantics)

| Opération | GraphML (APOC) | JSON-LD (neosemantics) |
|---|---|---|
| Importation | `CALL apoc.import.graphml(...)` | `CALL n10s.rdf.import.fetch(...)` |
| Exportation | `CALL apoc.export.graphml.all(...)` | Graph JSON-LD via endpoint RDF |
| Plugin requis | APOC Core | neosemantics (n10s) |
| Spécificité | Structure de graphe pure | Modèle sémantique (RDF) |
