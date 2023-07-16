import json

import joblib
from fastapi import APIRouter, HTTPException

from services.predict import chatGPT
from models.prediction import (
    RecommendedGame,
    GPTInput
)

router = APIRouter()


## Change this portion for other types of models
## Add the correct type hinting when completed
def get_recommendations(data_point):
    return chatGPT(data_point)


def make_list(gpt_answer):
    games = gpt_answer.strip().split("\n")
    return [game.split(". ")[1] for game in games]


@router.post(
    "/predict",
    response_model=RecommendedGame,
    name="predict:get-input",
)
async def gpt_recommend(data_input: GPTInput):

    if not data_input:
        raise HTTPException(status_code=404, detail="'data_input' argument invalid!")
    try:
        user_data = data_input.get_user_data()
        recommendations = get_recommendations(user_data)
        print(recommendations)
        recommendations = make_list(recommendations)

    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Exception: {err}")

    return RecommendedGame(games=recommendations)