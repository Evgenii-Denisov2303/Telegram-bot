from .facts import router as facts_router
from .photos import router as photos_router
from .fun import router as fun_router
from .survey import router as survey_router
from .useful import router as useful_router
from .menu import router as menu_router


def get_routers():
    return [
        facts_router,
        photos_router,
        fun_router,
        survey_router,
        useful_router,
        menu_router,
    ]
