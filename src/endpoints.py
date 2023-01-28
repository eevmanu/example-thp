import logging
from typing import Any
from http import HTTPStatus

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import select

from src.models import User, Audio
from src.schema import UserOut, UserIn, UserSearchIn
from src.schema import AudioOut, AudioIn, AudioSearchIn
from src.settings import cl_settings
from src.deps import get_db
from src.crud import user_crud, audio_crud


logging.basicConfig(
    level=cl_settings.LOGGING_LEVEL,
    format=cl_settings.LOGGING_FORMAT,
    style=cl_settings.LOGGING_STYLE,
)
logger = logging.getLogger(__name__)


user_router = APIRouter(prefix="/users", tags=["users"])
audio_router = APIRouter(prefix="/audios", tags=["audios"])


# read multiple users
@user_router.get(
    path="",
    name="users:read-users",
    response_model=list[UserOut],
    status_code=HTTPStatus.OK,
)
async def get_users(
    db: Session = Depends(get_db)
) -> list[UserOut]:
    users : list[User] = user_crud.get_multi(db)
    users_out : list[UserOut] = []
    for u in users:
        u_out = UserOut(
            id=u.id,
            name=u.name,
            email=u.email,
            address=u.address,
            image=u.image,
        )
        # u_out = UserOut(**u.__dict__)
        users_out.append(u_out)
    return users_out


# read user
@user_router.get(
    path="/{user_id}",
    name="users:read-user",
    # response_model=UserOut,
    status_code=HTTPStatus.OK,
)
async def get_user(
    user_id : int,
    db : Session = Depends(get_db)
# ) -> UserOut:
) -> Any:
    user : User | None = user_crud.get(db, user_id)
    if user is None:
        # return {"error": "user not found"}
        return JSONResponse(
            {"error": "user not found"},
            status_code=HTTPStatus.NOT_FOUND
        )
    return UserOut(
        id=user.id,
        name=user.name,
        email=user.email,
        address=user.address,
        image=user.image,
    )


# create user
@user_router.post(
    path="",
    name="users:create-user",
    response_model=UserOut,
    status_code=HTTPStatus.OK,
)
async def create_user(
    *,
    db : Session = Depends(get_db),
    user_in : UserIn
) -> UserOut:
    # TODO validate no other user has that email
    user = user_crud.create(db, user_in)
    # from pprint import pprint
    # pprint(user)
    # 👇 do not works when running test if you don't explicit log or print the variable
    # return UserOut(**user.__dict__)
    return UserOut(
        id=user.id,
        name=user.name,
        email=user.email,
        address=user.address,
        image=user.image,
    )


# full update user
@user_router.put(
    path="/{user_id}",
    name="users:full-update-user",
    response_model=UserOut,
    status_code=HTTPStatus.OK,
)
async def full_update_user(
    user_id : int,
    *,
    db : Session = Depends(get_db),
    user_in : UserIn,
) -> UserOut:
    user = user_crud.full_update(db, user_id, user_in)
    # return UserOut(**user.__dict__)
    return UserOut(
        id=user.id,
        name=user.name,
        email=user.email,
        address=user.address,
        image=user.image,
    )


# TODO partial update user with patch
# weaken the validations on schema.UserIn


# delete user
@user_router.delete(
    path="/{user_id}",
    name="users:delete-user",
    status_code=HTTPStatus.OK,
)
async def delete_user(
    user_id : int,
    db : Session = Depends(get_db),
) -> Any:
    user_crud.delete(db, user_id)
    return {"ok": "👌"}


# search user by id, name, email and address
@user_router.post(
    path="/search",
    name="users:search-user",
    response_model=list[UserOut],
    status_code=HTTPStatus.OK,
)
async def search_users(
    *,
    db : Session = Depends(get_db),
    user_search_in : UserSearchIn,
) -> Any:
    users = user_crud.search(db, user_search_in)
    users_out : list[UserOut] = []
    for u in users:
        u_out = UserOut(
            id=u.id,
            name=u.name,
            email=u.email,
            address=u.address,
            image=u.image,
        )
        # u_out = UserOut(**u.__dict__)
        users_out.append(u_out)
    return users_out


# --------------------------------------------------------------------------------

# read multiple audio
@audio_router.get(
    path="",
    name="audios:read-audios",
    response_model=list[AudioOut],
    status_code=HTTPStatus.OK,
)
async def get_audios(
    db: Session = Depends(get_db)
) -> list[AudioOut]:
    audios : list[Audio] = audio_crud.get_multi(db)
    audios_out : list[AudioOut] = []
    for a in audios:
        a_out = AudioOut(
            id=a.id,
            session_id=a.session_id,
            ticks=a.ticks,
            selected_tick=a.selected_tick,
            step_count=a.step_count,
        )
        # u_out = AudioOut(**u.__dict__)
        audios_out.append(a_out)
    return audios_out


# read audio
@audio_router.get(
    path="/{audio_id}",
    name="audios:read-audio",
    # response_model=AudioOut,
    status_code=HTTPStatus.OK,
)
async def get_audio(
    audio_id : int,
    db : Session = Depends(get_db)
) -> Any:
    audio : Audio | None = audio_crud.get(db, audio_id)
    if audio is None:
        return {"error": "audio not found"}
    return AudioOut(
        id=audio.id,
        session_id=audio.session_id,
        ticks=audio.ticks,
        selected_tick=audio.selected_tick,
        step_count=audio.step_count,
    )


# create audio
@audio_router.post(
    path="",
    name="audios:create-audio",
    status_code=HTTPStatus.OK,
)
async def create_audio(
    *,
    db : Session = Depends(get_db),
    audio_in : AudioIn
) -> Any:
    if audio_crud.exist_by_session_id(db, audio_in.session_id):
        return {"error": f"audio with {audio_in.session_id=} already exists"}
    audio : Audio = audio_crud.create(db, audio_in)
    logger.info(f"{audio=}")
    return AudioOut(**audio.__dict__)


# full update audio
@audio_router.put(
    path="/{audio_id}",
    name="audios:full-update-audio",
    response_model=AudioOut,
    status_code=HTTPStatus.OK,
)
async def full_update_audio(
    audio_id : int,
    *,
    db : Session = Depends(get_db),
    audio_in : AudioIn,
) -> AudioOut:
    audio = audio_crud.full_update(db, audio_id, audio_in)
    return AudioOut(**audio.__dict__)


# TODO partial update user with patch
# weaken the validations on schema.AudioIn


# delete audio
@audio_router.delete(
    path="/{audio_id}",
    name="audios:delete-audio",
    status_code=HTTPStatus.OK,
)
async def delete_audio(
    audio_id : int,
    db : Session = Depends(get_db),
) -> Any:
    audio_crud.delete(db, audio_id)
    return {"ok": "👌"}


# search audio by session_id
@audio_router.post(
    path="/search",
    name="audios:search-audio",
    response_model=list[AudioOut],
    status_code=HTTPStatus.OK,
)
async def search_audios(
    *,
    db : Session = Depends(get_db),
    audio_search_in : AudioSearchIn,
) -> Any:
    audios : list[Audio] = audio_crud.search(db, audio_search_in)
    audios_out : list[AudioOut] = []
    for a in audios:
        a_out = AudioOut(
            id=a.id,
            session_id=a.session_id,
            ticks=a.ticks,
            selected_tick=a.selected_tick,
            step_count=a.step_count,
        )
        audios_out.append(a_out)
    return audios_out


# --------------------------------------------------------------------------------

api_router = APIRouter()
api_router.include_router(router=user_router)
api_router.include_router(router=audio_router)
