import logging

from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete, cast, Float
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.dialects import postgresql


from src.settings import cl_settings
from src.models import User, Audio
from src.schema import UserIn, UserSearchIn, AudioIn, AudioSearchIn


# TODO move logging setup to one module
logging.basicConfig(
    level=cl_settings.LOGGING_LEVEL,
    format=cl_settings.LOGGING_FORMAT,
    style=cl_settings.LOGGING_STYLE,
)
logger = logging.getLogger(__name__)


class UserCRUD():

    def __init__(self) -> None:
        pass

    def get_multi(
        self,
        db: Session,
        # *,
        # skip : int = 0,
        # limit: int = 0,
    ) -> list[User]:
        # cursor_result =
        return db.execute(select(User)).scalars().all()

    def get(
        self,
        db: Session,
        user_id : int,
    ) -> User | None:
        try:
            user = db.execute(
                select(User)
                .where(User.id == user_id)
            ).scalar_one()
        except (NoResultFound, MultipleResultsFound):
            return None
        return user

    def create(
        self,
        db: Session,
        user_in: UserIn,
    ) -> User:
        # user = User(
        #     name=user_in.name,
        #     email=user_in.email,
        #     address=user_in.address,
        #     image=user_in.image,
        # )
        user = User(**user_in.dict())
        db.add(user)
        db.commit()
        # logger.info(f"{user=}")
        return user

    def full_update(
        self,
        db: Session,
        user_id : int,
        user_in: UserIn,
    ) -> User:
        db.execute(
            update(User)
            .where(User.id == user_id)
            .values(
                name=user_in.name,
                email=user_in.email,
                address=user_in.address,
                image=user_in.image,
            )
        )
        db.commit()
        return db.execute(
            select(User)
            .where(User.id == user_id)
        ).scalar_one()

    # def partial_update(self):
    #     ...

    def delete(
        self,
        db: Session,
        user_id : int,
    ) -> None:
        db.execute(
            delete(User)
            .where(User.id == user_id)
        )
        db.commit()

    def search(
        self,
        db: Session,
        user_search_in: UserSearchIn,
    ) -> list[User]:
        stmt = select(User)
        if user_search_in.id is not None:
            stmt = stmt.where(User.id == user_search_in.id)
        if user_search_in.email is not None:
            stmt = stmt.where(User.email == user_search_in.email)
        if user_search_in.address is not None:
            # TODO to improve, instead of contains, use similarity
            stmt = stmt.where(User.address.contains(user_search_in.address))
        return db.execute(stmt).scalars().all()


class AudioCRUD():
    def __init__(self) -> None:
        pass

    def get_multi(
        self,
        db: Session,
        # *,
        # skip : int = 0,
        # limit: int = 0,
    ) -> list[Audio]:
        return db.execute(select(Audio)).scalars().all()

    def get(
        self,
        db: Session,
        audio_id : int,
    ) -> Audio | None:
        try:
            audio = db.execute(
                select(Audio)
                .where(Audio.id == audio_id)
            ).scalar_one()
        except (NoResultFound, MultipleResultsFound):
            return None
        return audio


    def exist_by_session_id(
        self,
        db: Session,
        session_id: int,
    ) -> bool:
        try:
            db.execute(select(Audio).where(Audio.session_id == session_id)).one()
        except (NoResultFound, MultipleResultsFound):
            return False
        return True


    def create(
        self,
        db: Session,
        audio_in: AudioIn,
    ) -> Audio:
        audio = Audio(**audio_in.dict())
        db.add(audio)
        db.commit()
        return audio


    def full_update(
        self,
        db: Session,
        audio_id : int,
        audio_in : AudioIn,
    ):
        db.execute(
            update(Audio)
            .where(Audio.id == audio_id)
            .values(
                session_id=audio_in.session_id,
                ticks=audio_in.ticks,
                selected_tick=audio_in.selected_tick,
                step_count=audio_in.step_count,
            )
        )
        db.commit()
        return db.execute(
            select(Audio)
            .where(Audio.id == audio_id)
        ).scalar_one()


    def delete(
        self,
        db: Session,
        audio_id: int,
    ) -> None:
        db.execute(
            delete(Audio)
            .where(Audio.id == audio_id)
        )
        db.commit()

    def search(
        self,
        db: Session,
        audio_search_in: AudioSearchIn,
    ) -> list[Audio]:
        stmt = select(Audio)
        if audio_search_in.session_id is not None:
            stmt = stmt.where(Audio.session_id == audio_search_in.session_id)
        return db.execute(stmt).scalars().all()


user_crud : UserCRUD = UserCRUD()
audio_crud : AudioCRUD = AudioCRUD()
