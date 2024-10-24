import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from secret.config import DATABASE_URL

from sqlalchemy import (
    CheckConstraint,
    create_engine,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    func,
    Integer,
    PrimaryKeyConstraint,
    String,
)
from sqlalchemy.orm import sessionmaker, declarative_base, Mapped
from sqlalchemy.inspection import inspect

# Create a new SQLAlchemy engine
engine = create_engine(DATABASE_URL)

Base = declarative_base()


class Player(Base):
    __tablename__ = "player"  # Name of the table

    player_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    is_human = Column(Boolean, nullable=False, default=True)
    strategy = Column(String, nullable=True)
    description = Column(String, nullable=True)
    difficulty = Column(Integer, nullable=True)
    registration_date = Column(DateTime(timezone=True), server_default=func.now())


class GameRule(Base):
    __tablename__ = "game_rule"

    game_rule_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)


class SetOfRules(Base):
    __tablename__ = "set_of_rules"

    set_of_rules_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)


class IsRuleOf(Base):  # Many to many
    __tablename__ = "is_rule_of"

    set_of_rules_id = Column(
        Integer,
        ForeignKey("set_of_rules.set_of_rules_id", ondelete="CASCADE"),
        nullable=False,
    )
    game_rule_id = Column(
        Integer,
        ForeignKey("game_rule.game_rule_id", ondelete="CASCADE"),
        nullable=False,
    )
    __table_args__ = (PrimaryKeyConstraint("set_of_rules_id", "game_rule_id"),)


class Game(Base):
    __tablename__ = "game"

    game_id = Column(Integer, primary_key=True, autoincrement=True)
    set_of_rules_id = Column(
        Integer,
        ForeignKey("set_of_rules.set_of_rules_id", ondelete="CASCADE"),
        nullable=False,
    )
    played_at = Column(DateTime(timezone=True), server_default=func.now())
    nb_participants = Column(Integer, nullable=False)


class Participant(Base):
    __tablename__ = "participant"

    game_id = Column(
        Integer, ForeignKey("game.game_id", ondelete="CASCADE"), nullable=False
    )
    player_id = Column(
        Integer, ForeignKey("player.player_id", ondelete="CASCADE"), nullable=False
    )
    __table_args__ = (PrimaryKeyConstraint("game_id", "player_id"),)

    turn_order = Column(Integer, nullable=False)
    __table_args__ = (
        PrimaryKeyConstraint("game_id", "player_id"),
        CheckConstraint("turn_order IN (1, 2, 3, 4)", name="check_turn_order"),
    )
    score = Column(
        Integer, nullable=False, default=0
    )  # 0 if the player is human -> score of the selected agent
    nb_moves = Column(Integer, nullable=False, default=0)
    is_winner = Column(Boolean, nullable=False, default=False)


# Create all tables in the database
Base.metadata.create_all(engine)


def display_schema():
    inspector = inspect(engine)
    for table_name in inspector.get_table_names():
        print(f"Table: {table_name}")
        columns = inspector.get_columns(table_name)
        for column in columns:
            print(
                f"  Column: {column['name']}, Type: {column['type']}, Nullable: {column['nullable']}"
            )


def add_players():
    Session = sessionmaker(bind=engine)
    session = Session()

    try:

        human_players = [
            Player(name="Zoé"),
            Player(name="Charlotte"),
            Player(name="Katia"),
            Player(name="Daniil"),
        ]

        session.add_all(human_players)
        session.commit()
        print("Players have been added successfully.")

    except Exception as e:
        print(f"Error during adding players: {e}")
        session.rollback()

    finally:
        session.close()


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    display_schema()
    # add_players()
