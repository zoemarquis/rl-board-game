import enum
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from secret.config import DATABASE_URL

from sqlalchemy import (
    CheckConstraint,
    create_engine,
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    func,
    Integer,
    PrimaryKeyConstraint,
    String,
    text,
)
from sqlalchemy.orm import sessionmaker, declarative_base, Mapped
from sqlalchemy.inspection import inspect

# Create a new SQLAlchemy engine
engine = create_engine(DATABASE_URL)

Base = declarative_base()  


class PlayerType(enum.Enum):
    HUMAN = "human"
    AGENT = "agent"


class Player(Base):
    __tablename__ = "player"  # Name of the table

    player_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    type = Column(Enum(PlayerType), nullable=False, default=PlayerType.HUMAN)
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
        CheckConstraint('turn_order IN (1, 2, 3, 4)', name='check_turn_order')
    )
    score = Column(Integer, nullable=False, default=0) # 0 if the player is human -> score of the selected agent
    nb_moves = Column(Integer, nullable=False, default=0)
    is_winner = Column(Boolean, nullable=False, default=False)

# Create all tables in the database
Base.metadata.create_all(engine)

# Function to display the schema
def display_schema():
    inspector = inspect(engine)
    for table_name in inspector.get_table_names():
        print(f"Table: {table_name}")
        columns = inspector.get_columns(table_name)
        for column in columns:
            print(
                f"  Column: {column['name']}, Type: {column['type']}, Nullable: {column['nullable']}"
            )



# Fonction principale pour ajouter des joueurs
def add_players():
    # Créer une session
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Créer des instances de Player
        human_players = [
            Player(name="Zoé", type=PlayerType.HUMAN),
            Player(name="Charlotte", type=PlayerType.HUMAN),
            Player(name="Katia", type=PlayerType.HUMAN),
            Player(name="Daniil", type=PlayerType.HUMAN),
        ]

        # Ajouter les joueurs à la session
        session.add_all(human_players)

        # Committer les changements à la base de données
        session.commit()
        print("Les joueurs ont été ajoutés avec succès.")

    except Exception as e:
        print(f"Erreur lors de l'ajout des joueurs : {e}")
        session.rollback()  # Annuler les changements en cas d'erreur

    finally:
        session.close()  # Fermer la session


if __name__ == "__main__":
    # Créer toutes les tables dans la base de données
    Base.metadata.create_all(engine)
    
    # Ajouter des joueurs
    add_players()
