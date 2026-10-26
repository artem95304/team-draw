from fastapi.testclient import TestClient

from app_final import app


client = TestClient(app)


def setup_function():
    client.delete("/participants")


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_add_single_participant():
    response = client.post(
        "/participants", params={"text": "Саша Иванов"}
    )

    assert response.status_code == 201
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Саша Иванов"


def test_add_multiple_participants():
    response = client.post(
        "/participants",
        params={"text": "Аня Боря Аня", "split_by_spaces": True},
    )

    assert response.status_code == 201
    participants = response.json()
    nicknames = [person["nickname"] for person in participants]
    assert nicknames == ["Аня 1", "Боря 1", "Аня 2"]
    assert len({person["id"] for person in participants}) == 3
    assert client.get("/participants").json() == participants


def test_clear_participants():
    client.post("/participants", params={"text": "Аня"})

    response = client.delete("/participants")

    assert response.status_code == 200
    assert client.get("/participants").json() == []


def test_draw_teams():
    client.post(
        "/participants",
        params={"text": "Аня Боря Вика Глеб Даша", "split_by_spaces": True},
    )
    original = client.get("/participants").json()
    response = client.post("/draw/teams", params={"team_count": 2})

    assert response.status_code == 200
    teams = response.json()["teams"]
    assert sorted(len(team) for team in teams) == [2, 3]

    result = teams[0] + teams[1]
    expected_ids = sorted(person["id"] for person in original)
    actual_ids = sorted(person["id"] for person in result)
    assert actual_ids == expected_ids
    assert client.get("/participants").json() == original


def test_draw_pairs_even():
    client.post(
        "/participants",
        params={"text": "Аня Боря Вика Глеб", "split_by_spaces": True},
    )
    original = client.get("/participants").json()
    response = client.post("/draw/pairs")

    assert response.status_code == 200
    data = response.json()
    assert [len(pair) for pair in data["pairs"]] == [2, 2]
    assert data["unpaired"] is None

    result = data["pairs"][0] + data["pairs"][1]
    expected_ids = sorted(person["id"] for person in original)
    actual_ids = sorted(person["id"] for person in result)
    assert actual_ids == expected_ids
    assert client.get("/participants").json() == original


def test_draw_pairs_odd():
    client.post(
        "/participants",
        params={"text": "Аня Боря Вика Глеб Даша", "split_by_spaces": True},
    )
    original = client.get("/participants").json()
    response = client.post("/draw/pairs")

    assert response.status_code == 200
    data = response.json()
    assert [len(pair) for pair in data["pairs"]] == [2, 2]
    assert data["unpaired"] is not None

    result = data["pairs"][0] + data["pairs"][1] + [data["unpaired"]]
    expected_ids = sorted(person["id"] for person in original)
    actual_ids = sorted(person["id"] for person in result)
    assert actual_ids == expected_ids
    assert client.get("/participants").json() == original


def test_invalid_input():
    response = client.post("/participants", params={"text": ""})
    assert response.status_code == 400

    response = client.post("/draw/teams", params={"team_count": 2})
    assert response.status_code == 400

    response = client.post("/draw/pairs")
    assert response.status_code == 400

    client.post(
        "/participants",
        params={"text": "Аня Боря", "split_by_spaces": True},
    )
    response = client.post("/draw/teams", params={"team_count": 3})
    assert response.status_code == 400
