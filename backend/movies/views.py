from rest_framework.views import APIView
from rest_framework.response import Response
from neo4j_utils import db

class MovieListView(APIView):
    def get(self, request):
        query = "MATCH (m:Movie) RETURN m.title AS title, m.year AS year, m.rating AS rating"
        results = db.query(query)
        movies = [
            {"title": record["title"], "year": record["year"], "rating": record["rating"]}
            for record in results
        ]
        return Response(movies)

class GraphDataView(APIView):
    def get(self, request):
        # Pobieramy relacje, ale ograniczamy się do istotnych dla wizualizacji
        query = """
        MATCH (n)-[r]->(m)
        WHERE NOT n:User AND NOT m:User
        RETURN n, r, m LIMIT 150
        """
        results = db.query(query)
        
        nodes = []
        links = []
        node_ids = set()

        for record in results:
            source = record['n']
            target = record['m']
            rel = record['r']

            # Funkcja pomocnicza do nazw
            def get_node_name(node):
                return node.get('name') or node.get('title') or node.get('username') or "Unnamed"

            # Dodaj węzeł źródłowy
            if source.element_id not in node_ids:
                nodes.append({
                    "id": source.element_id, 
                    "label": list(source.labels)[0], 
                    "name": get_node_name(source)
                })
                node_ids.add(source.element_id)

            # Dodaj węzeł docelowy
            if target.element_id not in node_ids:
                nodes.append({
                    "id": target.element_id, 
                    "label": list(target.labels)[0], 
                    "name": get_node_name(target)
                })
                node_ids.add(target.element_id)

            # Dodaj relację
            links.append({
                "source": source.element_id,
                "target": target.element_id,
                "type": rel.type
            })

        return Response({"nodes": nodes, "links": links})