import os
from dataclasses import dataclass
from dotenv import load_dotenv, find_dotenv


if find_dotenv():
    load_dotenv()


@dataclass(frozen=True)
class Settings:
    bot_token: str
    cat_api_url: str
    cat_facts_api_url: str
    translate_api_url: str


def load_settings() -> Settings:
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        raise ValueError(
            "BOT_TOKEN is missing. Set it in Railway Variables or .env."
        )

    return Settings(
        bot_token=bot_token,
        cat_api_url=os.getenv(
            "CAT_API_KEY",
            "https://api.thecatapi.com/v1/images/search",
        ),
        cat_facts_api_url=os.getenv(
            "CAT_FACTS_API_KEY",
            "https://catfact.ninja/fact",
        ),
        translate_api_url=os.getenv(
            "TRANSLATE_API_KEY",
            "https://translate.googleapis.com/translate_a/single",
        ),
    )


DEFAULT_COMMANDS = (
    ("start", "Запустить котика-ботика"),
    ("help", "Помощь по функциям"),
    ("survey", "Опрос"),
)


CAT_PHOTOS = {
    "Манечка": [
        "utils/cat_photos/Manechka.jpg",
        "utils/cat_photos/Manechka1.jpg",
        "utils/cat_photos/Manechka3.jpg",
        "utils/cat_photos/Manechka4.jpg",
    ],
    "Цезарь": [
        "utils/cat_photos/Cezar.jpg",
        "utils/cat_photos/Cezar1.jpg",
        "utils/cat_photos/Cezar2.jpg",
    ],
    "Шотландец": [
        "utils/cat_photos/shot.jpg",
        "utils/cat_photos/shot1.jpg",
        "utils/cat_photos/shot2.jpg",
    ],
}
