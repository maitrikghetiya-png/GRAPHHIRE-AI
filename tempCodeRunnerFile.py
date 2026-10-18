import os
from typing import Dict, List, Any
from dotenv import load_dotenv
from falkordb import FalkorDB

load_dotenv()

class GraphEngine:
    def __init__(self):
        host = os.getenv("FALKORDB_HOST", "localhost")
        port = int(os.getenv("FALKORDB_PORT", 6379))
        password = os.getenv("FALKORDB_PASSWORD", None)
        self.graph_name = os.getenv("FALKORDB_GRAPH_NAME", "GraphHire")

        try:
            self.db = FalkorDB(host=host, port=port, password=password if password else None)
            self.graph = self.db.select_graph(self.graph_name)
        except Exception as e:
            raise ConnectionError(f"Failed to connect to FalkorDB instance at {host}:{port}: {e}")

    def seed_data(self) -> None:
        """Clears existing graph and populates realistic sample data."""
        clear_query = "MATCH (n) DETACH DELETE n"
        try:
            self.graph.query(clear_query)
        except Exception as e:
            raise RuntimeError(f"Error resetting database: {e}")

        seed_query = """
        CREATE 
          (s1:Student {name: 'Aarav'}),
          (s2:Student {name: 'Ananya'}),

          (k1:Skill {name: 'Python'}),
          (k2:Skill {name: 'SQL'}),
          (k3:Skill {name: 'Docker'}),
          (k4:Skill {name: 'React'}),

          (j1:Job {title: 'Backend Engineer'}),
          (j2:Job {title: 'Full Stack Engineer'}),

          (c1:Course {name: 'Docker Mastery'}),
          (c2:Course {name: 'React Foundations'}),

          (s1)-[:HAS_SKILL]->(k1),
          (s1)-[:HAS_SKILL]->(k2),
          
          (s2)-[:HAS_SKILL]->(k1),
          (s2)-[:HAS_SKILL]->(k4),

          (j1)-[:REQUIRES]->(k1),
          (j1)-[:REQUIRES]->(k2),
          (j1)-[:REQUIRES]->(k3),

          (j2)-[:REQUIRES]->(k1),
          (j2)-[:REQUIRES]->(k4),
          (j2)-[:REQUIRES]->(k3),

          (c1)-[:TEACHES]->(k3),
          (c2)-[:TEACHES]->(k4)
        """
        try:
            self.graph.query(seed_query)
        except Exception as e:
            raise RuntimeError(f"Error seeding database: {e}")

    def get_recommendations(self, student_name: str) -> List[Dict[str, Any]]:
        """
        Calculates job matches and recommends courses for missing skills using graph logic.
        """
        query = """
        MATCH (s:Student {name: $student_name})
        MATCH (j:Job)-[:REQUIRES]->(reqSkill:Skill)
        WITH s, j, collect(reqSkill.name) AS required_skills
        OPTIONAL MATCH (s)-[:HAS_SKILL]->(ownedSkill:Skill) WHERE ownedSkill.name IN required_skills
        WITH s, j, required_skills, collect(ownedSkill.name) AS matched_skills
        WITH j, required_skills, matched_skills,
             [k IN required_skills WHERE NOT k IN matched_skills] AS missing_skills
        OPTIONAL MATCH (c:Course)-[:TEACHES]->(missingSkill:Skill) WHERE missingSkill.name IN missing_skills
        RETURN 
          j.title AS job_title,
          round((toFLoat(size(matched_skills)) / size(required_skills)) * 100) AS match_percent,
          matched_skills,
          missing_skills,
          collect(DISTINCT c.name) AS recommended_courses
        ORDER BY match_percent DESC
        """
        params = {"student_name": student_name}
        
        try:
            result = self.graph.query(query, params)
        except Exception as e:
            raise RuntimeError(f"Error executing recommendation query for '{student_name}': {e}")

        recommendations = []
        for row in result.result_set:
            recommendations.append({
                "job_title": row[0],
                "match_percent": float(row[1]) if row[1] is not None else 0.0,
                "matched_skills": row[2] if row[2] else [],
                "missing_skills": row[3] if row[3] else [],
                "recommended_courses": [course for course in row[4] if course is not None]
            })

        return recommendations


if __name__ == "__main__":
    engine = GraphEngine()
    print("Seeding database...")
    engine.seed_data()
    print("Fetching recommendations for 'Aarav'...")
    recs = engine.get_recommendations("Aarav")
    import json
    print(json.dumps(recs, indent=2))