import logging
import os
import random
from uuid import uuid4
from fastapi import FastAPI, HTTPException


APP_VERSION = os.getenv("APP_VERSION", "0.1.0")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Team Draw", version=APP_VERSION)
participants = []


def make_teams(people, team_count):
    shuffled = people.copy()
    random.shuffle(shuffled)
    teams = [[] for _ in range(team_count)]

    for index, person in enumerate(shuffled):
        teams[index % team_count].append(person)

    return teams


def make_pairs(people):
    shuffled = people.copy()
    random.shuffle(shuffled)

    unpaired = None
    if len(shuffled) % 2:
        unpaired = shuffled.pop()

    pairs = []
    for index in range(0, len(shuffled), 2):
        pairs.append(shuffled[index:index + 2])

    return pairs, unpaired


@app.get("/health")
def health():
    logger.info("Health check")
    return {"status": "ok"}


@app.get("/version")
def version():
    logger.info("Version requested")
    return {"version": APP_VERSION}


@app.get("/participants")
def get_participants():
    return participants


@app.post("/participants", status_code=201)
def add_participants(text: str, split_by_spaces: bool = False):
    text = text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Введите хотя бы одно имя")

    if split_by_spaces:
        names = text.split()
    else:
        names = [text]

    added = []
    for name in names:
        number = 1
        for participant in participants:
            if participant["name"] == name:
                number += 1

        participant = {
            "id": str(uuid4()),
            "name": name,
            "nickname": f"{name} {number}",
        }
        participants.append(participant)
        added.append(participant)

    logger.info("Added participants: %s", len(added))
    return added


@app.delete("/participants")
def clear_participants():
    participants.clear()
    logger.info("Participants cleared")
    return {"message": "Список участников очищен"}


@app.post("/draw/teams")
def draw_teams(team_count: int):
    if not participants:
        raise HTTPException(
            status_code=400, detail="Сначала добавьте участников"
        )
    if team_count < 1 or team_count > len(participants):
        raise HTTPException(
            status_code=400,
            detail=f"Укажите число команд от 1 до {len(participants)}",
        )

    teams = make_teams(participants, team_count)
    logger.info("Created teams: %s", team_count)
    return {"teams": teams}


@app.post("/draw/pairs")
def draw_pairs():
    if not participants:
        raise HTTPException(
            status_code=400, detail="Сначала добавьте участников"
        )

    pairs, unpaired = make_pairs(participants)
    logger.info("Created pairs: %s", len(pairs))
    return {"pairs": pairs, "unpaired": unpaired}
