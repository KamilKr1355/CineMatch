from rest_framework.views import APIView
from rest_framework.response import Response
from neo4j_utils import db


class ShortestPathView(APIView):
    def get(self, request):
        start_node = request.query_params.get('start')
        end_node = request.query_params.get('end')

        if not start_node or not end_node:
            return Response({"error": "Podaj obie nazwy"}, status=400)

        query = """
        MATCH (n1), (n2)
        WHERE (n1.name = $start OR n1.title = $start)
          AND (n2.name = $end OR n2.title = $end)
        MATCH p = shortestPath((n1)-[*..15]-(n2))
        WHERE ALL(x IN nodes(p) WHERE NOT x:User)
        RETURN p, length(p) AS hops
        """

        results = db.query(query, {"start": start_node, "end": end_node})

        if not results:
            return Response({"error": "Nie znaleziono połączenia filmowego"}, status=404)

        path = results[0]['p']
        hops = results[0]['hops']

        def get_n_name(node):
            return node.get('name') or node.get('title') or "Unknown"

        nodes = []
        for node in path.nodes:
            nodes.append({
                "id": node.element_id,
                "name": get_n_name(node),
                "label": list(node.labels)[0]
            })

        links = []
        explanation = []
        for rel in path.relationships:
            s_name = get_n_name(rel.start_node)
            e_name = get_n_name(rel.end_node)
            role = rel.get('role', '')
            t = rel.type
            if role:
                explanation.append(f"{s_name} —[{t}: {role}]→ {e_name}")
            else:
                explanation.append(f"{s_name} —[{t}]→ {e_name}")
            links.append({
                "source": rel.start_node.element_id,
                "target": rel.end_node.element_id,
                "type": t
            })

        return Response({
            "nodes": nodes,
            "links": links,
            "explanation": explanation,
            "hops": hops
        })


class PersonalizedRecommendationView(APIView):
    def post(self, request):
        interests = request.data.get('interests', [])
        if not interests:
            return Response([])

        query = """
        MATCH (n)
        WHERE (n.name IN $interests OR n.title IN $interests)
        MATCH (n)-[r:ACTED_IN|DIRECTED|BELONGS_TO]-(m:Movie)
        WHERE NOT m.title IN $interests
        WITH m, n, type(r) AS rel_type,
             CASE type(r)
               WHEN 'ACTED_IN'   THEN 'gra w'
               WHEN 'DIRECTED'   THEN 'rezyseruje'
               WHEN 'BELONGS_TO' THEN 'gatunek'
               ELSE type(r)
             END AS rel_label,
             labels(n)[0] AS node_type
        WITH m,
             collect({ name: n.name, rel: rel_label, node_type: node_type }) AS connections,
             count(n) AS score
        RETURN m.title AS title, m.year AS year, m.rating AS rating,
               score, connections
        ORDER BY score DESC, m.rating DESC
        LIMIT 8
        """
        results = db.query(query, {"interests": interests})

        recommendations = []
        for record in results:
            connections = record["connections"]

            actors    = [c["name"] for c in connections if c["node_type"] == "Person" and c["rel"] == "gra w"]
            directors = [c["name"] for c in connections if c["node_type"] == "Person" and c["rel"] == "rezyseruje"]
            genres    = [c["name"] for c in connections if c["node_type"] == "Genre"]

            reason_parts = []
            if actors:
                if len(actors) == 1:
                    reason_parts.append(f"{actors[0]} gra w tym filmie")
                else:
                    reason_parts.append(f"{', '.join(actors[:-1])} i {actors[-1]} grają w tym filmie")
            if directors:
                reason_parts.append(f"reżyseruje {directors[0]}")
            if genres:
                reason_parts.append(f"gatunek: {', '.join(genres)}")

            recommendations.append({
                "title":       record["title"],
                "year":        record["year"],
                "rating":      record["rating"],
                "score":       record["score"],
                "reasons":     reason_parts,
                "connections": len(connections),
            })

        return Response(recommendations)


class ActorRankingView(APIView):
    """PageRank-style ranking — aktorzy z największą liczbą filmów i połączeń."""
    def get(self, request):
        query = """
        MATCH (p:Person)-[:ACTED_IN]->(m:Movie)
        WITH p, count(m) AS film_count,
             avg(m.rating) AS avg_rating,
             collect(m.title) AS titles
        ORDER BY film_count DESC, avg_rating DESC
        LIMIT 10
        RETURN p.name AS name, film_count AS count,
               round(avg_rating * 10) / 10 AS avg_rating, titles
        """
        results = db.query(query)
        return Response([
            {
                "name": r["name"],
                "count": r["count"],
                "avg_rating": r["avg_rating"],
                "titles": r["titles"]
            }
            for r in results
        ])


class CommonElementsView(APIView):
    """Co łączy dwa filmy? Wspólni aktorzy, reżyser, gatunek."""
    def get(self, request):
        movie1 = request.query_params.get('movie1')
        movie2 = request.query_params.get('movie2')
        if not movie1 or not movie2:
            return Response({"error": "Podaj movie1 i movie2"}, status=400)

        query = """
        MATCH (m1:Movie {title: $m1})<-[r1]-(x)-[r2]->(m2:Movie {title: $m2})
        RETURN x.name AS element, type(r1) AS rel1, type(r2) AS rel2,
               labels(x)[0] AS type
        """
        results = db.query(query, {"m1": movie1, "m2": movie2})
        connections = [
            {
                "element": r["element"],
                "type": r["type"],
                "rel1": r["rel1"],
                "rel2": r["rel2"]
            }
            for r in results
        ]
        return Response({"movie1": movie1, "movie2": movie2, "connections": connections})


class TimelineView(APIView):
    """Filmy z lat — opcjonalnie filtrowane po gatunku."""
    def get(self, request):
        genre = request.query_params.get('genre', None)

        if genre:
            query = """
            MATCH (m:Movie)-[:BELONGS_TO]->(g:Genre {name: $genre})
            OPTIONAL MATCH (d:Person)-[:DIRECTED]->(m)
            RETURN m.title AS title, m.year AS year, m.rating AS rating,
                   g.name AS genre, d.name AS director
            ORDER BY m.year ASC
            """
            results = db.query(query, {"genre": genre})
        else:
            query = """
            MATCH (m:Movie)
            OPTIONAL MATCH (m)-[:BELONGS_TO]->(g:Genre)
            OPTIONAL MATCH (d:Person)-[:DIRECTED]->(m)
            RETURN m.title AS title, m.year AS year, m.rating AS rating,
                   g.name AS genre, d.name AS director
            ORDER BY m.year ASC
            """
            results = db.query(query)

        movies = [
            {
                "title": r["title"],
                "year": r["year"],
                "rating": r["rating"],
                "genre": r["genre"],
                "director": r["director"]
            }
            for r in results
        ]
        return Response(movies)


class GenreStatsView(APIView):
    """Statystyki dla każdego gatunku."""
    def get(self, request):
        query = """
        MATCH (m:Movie)-[:BELONGS_TO]->(g:Genre)
        RETURN g.name AS genre,
               count(m) AS count,
               round(avg(m.rating) * 10) / 10 AS avg_rating,
               max(m.rating) AS top_rating,
               collect(m.title)[..3] AS sample_titles
        ORDER BY count DESC
        """
        results = db.query(query)
        return Response([
            {
                "genre": r["genre"],
                "count": r["count"],
                "avg_rating": r["avg_rating"],
                "top_rating": r["top_rating"],
                "sample_titles": r["sample_titles"]
            }
            for r in results
        ])


class SixDegreesQuizView(APIView):
    """
    Zwraca parę węzłów do quizu 'Six Degrees of Hollywood'
    wraz z prawdziwą długością najkrótszej ścieżki.
    """
    def get(self, request):
        query = """
        MATCH (p1:Person)-[:ACTED_IN]->(:Movie)<-[:ACTED_IN]-(p2:Person)
        WHERE p1 <> p2
        WITH p1, p2, rand() AS r
        ORDER BY r
        LIMIT 1
        MATCH path = shortestPath((p1)-[*..10]-(p2))
        WHERE ALL(x IN nodes(path) WHERE NOT x:User)
        RETURN p1.name AS actor1, p2.name AS actor2, length(path) AS hops
        """
        results = db.query(query)
        if not results:
            return Response({"error": "Brak danych"}, status=500)
        r = results[0]
        return Response({
            "actor1": r["actor1"],
            "actor2": r["actor2"],
            "hops": r["hops"]
        })