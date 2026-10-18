import pytest
from graph_engine import GraphEngine

def test_recommendations():
    try:
        engine = GraphEngine()
    except Exception as e:
        pytest.fail(f"Could not connect to FalkorDB instance: {e}")

    engine.seed_data()

    recommendations = engine.get_recommendations("Aarav")

    assert len(recommendations) > 0, "Recommendations should not be empty."

    backend_job = next((item for item in recommendations if item["job_title"] == "Backend Engineer"), None)
    assert backend_job is not None, "Backend Engineer job should be present."

    # Aarav has Python and SQL. Backend Engineer requires Python, SQL, Docker (2/3 = ~67%)
    assert backend_job["match_percent"] == 67.0
    assert "Python" in backend_job["matched_skills"]
    assert "SQL" in backend_job["matched_skills"]
    assert "Docker" in backend_job["missing_skills"]
    assert "Docker Mastery" in backend_job["recommended_courses"]

if __name__ == "__main__":
    test_recommendations()
    print("All backend graph engine tests passed successfully!")