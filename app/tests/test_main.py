from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# test top 2 of small dataset
def test_get_top_ids_x2():
    """Test with x=2 to get the top 2 numerical IDs"""
    with open("tests/small_test_data.txt", "rb") as file:
        response = client.post("/top-ids/?x=2", files={"file": ("test_data.txt", file)})

    assert response.status_code == 200
    data = response.json()
    assert "top_ids" in data
    assert len(data["top_ids"]) == 2
    assert set(data["top_ids"]) == {"55555555", "33333333"}  # Top 2 IDs

# test top 3 of the big dataset ( 100k lines )
def test_get_top_ids_x3():
    """Test with x=3 to get the top 3 numerical IDs"""
    with open("tests/test_data.txt", "rb") as file:
        response = client.post("/top-ids/?x=3", files={"file": ("test_data.txt", file)})

    assert response.status_code == 200
    data = response.json()
    assert "top_ids" in data
    assert len(data["top_ids"]) == 3
    assert set(data["top_ids"]) == {"83433056", "27101429", "74388036"}  # Top 3 IDs
