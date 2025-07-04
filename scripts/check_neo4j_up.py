from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
user = "neo4j"
password = "neo4jtest123"

try:
    driver = GraphDatabase.driver(uri, auth=(user, password))
    with driver.session() as session:
        result = session.run("RETURN 1")
        print("Connected:", result.single()[0])
    driver.close()
except Exception as e:
    print("Connection failed:", e)
