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
    UniqueConstraint,
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
    description = Column(String, nullable=True)
    strategy = Column(String, nullable=True)
    difficulty = Column(Integer, nullable=True)
    registration_date = Column(DateTime(timezone=True), server_default=func.now())
    nb_train_steps = Column(Integer, nullable=True)


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
    num_config = Column(Integer, nullable=False)


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
    nb_pawns = Column(Integer, nullable=False)


class Participant(Base):
    __tablename__ = "participant"

    participant_id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(Integer, ForeignKey("game.game_id", ondelete="CASCADE"), nullable=False)
    player_id = Column(Integer, ForeignKey("player.player_id", ondelete="CASCADE"), nullable=False)
    num_player_game = Column(Integer, nullable=False)
    action_stats = Column(Integer, ForeignKey("action_stats.stat_id", ondelete="CASCADE"), nullable=True)
    turn_order = Column(Integer, nullable=False)
    reward_action_agent = Column(Integer, nullable=False, default=0) # ancien score
    reward_rectified = Column(Integer, nullable=False)
    nb_moves = Column(Integer, nullable=False, default=0)
    is_winner = Column(Boolean, nullable=False, default=False)
    nb_actions_interdites = Column(Integer, nullable=False, default=0)
    nb_pawns_in_goal = Column(Integer, nullable=False, default=0)

class ActionStats(Base):
    __tablename__ = "action_stats"

    # Actions demandées par l'agent
    # Attention : pas forcément réalisées si l'action est impossible
    stat_id = Column(Integer, primary_key=True, autoincrement=True)
    nb_no_action_d = Column(Integer, nullable=False, default=0)
    nb_move_out_d = Column(Integer, nullable=False, default=0)
    nb_move_out_and_kill_d = Column(Integer, nullable=False, default=0)
    nb_move_forward_d = Column(Integer, nullable=False, default=0)
    nb_get_stuck_behind_d = Column(Integer, nullable=False, default=0)
    nb_enter_safezone_d = Column(Integer, nullable=False, default=0)
    nb_move_in_safe_zone_d = Column(Integer, nullable=False, default=0)
    nb_reach_goal_d = Column(Integer, nullable=False, default=0)
    nb_kill_d = Column(Integer, nullable=False, default=0)
    nb_reach_pied_escalier_d = Column(Integer, nullable=False, default=0)
    nb_avance_recule_pied_escalier_d = Column(Integer, nullable=False, default=0)
    nb_marche_1_d = Column(Integer, nullable=False, default=0)
    nb_marche_2_d = Column(Integer, nullable=False, default=0)
    nb_marche_3_d = Column(Integer, nullable=False, default=0)
    nb_marche_4_d = Column(Integer, nullable=False, default=0)
    nb_marche_5_d = Column(Integer, nullable=False, default=0)
    nb_marche_6_d = Column(Integer, nullable=False, default=0)

    # Actions effectuées par l'agent
    # Attention : pas forcément demandées par l'agent (action automatique)
    nb_no_action_e = Column(Integer, nullable=False, default=0)
    nb_move_out_e = Column(Integer, nullable=False, default=0)
    nb_move_out_and_kill_e = Column(Integer, nullable=False, default=0)
    nb_move_forward_e = Column(Integer, nullable=False, default=0)
    nb_get_stuck_behind_e = Column(Integer, nullable=False, default=0)
    nb_enter_safezone_e = Column(Integer, nullable=False, default=0)
    nb_move_in_safe_zone_e = Column(Integer, nullable=False, default=0)
    nb_reach_goal_e = Column(Integer, nullable=False, default=0)
    nb_kill_e = Column(Integer, nullable=False, default=0)
    nb_reach_pied_escalier_e = Column(Integer, nullable=False, default=0)
    nb_avance_recule_pied_escalier_e = Column(Integer, nullable=False, default=0)
    nb_marche_1_e = Column(Integer, nullable=False, default=0)
    nb_marche_2_e = Column(Integer, nullable=False, default=0)
    nb_marche_3_e = Column(Integer, nullable=False, default=0)
    nb_marche_4_e = Column(Integer, nullable=False, default=0)
    nb_marche_5_e = Column(Integer, nullable=False, default=0)
    nb_marche_6_e = Column(Integer, nullable=False, default=0)
    

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


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    display_schema()
    # add_players()
