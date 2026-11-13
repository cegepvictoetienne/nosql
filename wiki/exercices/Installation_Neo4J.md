## 1. Neo4J

```bash
cd ~
git clone https://github.com/cegepvictoetienne/neo4jdocker.git
cd neo4jdocker
cp .env.example .env
mkdir neo4j_data
mkdir neo4j_logs
mkdir neo4j_import
docker compose up -d
```

Se connecter : 

<http://localhost:7474/browser/>  

