from typing import Optional
from sqlmodel import Field, SQLModel, create_engine, Session, select, or_, Relationship
import os
import logging

from sqlalchemy import log as sqlalchemy_log

sqlalchemy_log._add_default_handler = lambda x: None

logging.basicConfig(format="\033[90m%(message)s\033[0m\n")

if os.path.exists("database_rel2.db"):
    os.remove("database_rel2.db")


class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str

    heroes: list["Hero"] = Relationship(back_populates="team")


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # index=True is used to create an index on the column
    # this makes the column faster to search
    # but slower to write
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)

    team_id: Optional[int] = Field(default=None, foreign_key="team.id")
    team: Optional[Team] = Relationship(back_populates="heroes")


sqlite_file_name = "database_rel2.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_heroes():
    with Session(engine) as session:
        team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
        team_z_force = Team(name="Z-Force", headquarters="Sister Margaret's Bar")

        hero_deadpond = Hero(
            name="Deadpond", secret_name="Dive Wilson", team=team_z_force
        )
        hero_rusty_man = Hero(
            name="Rusty-Man",
            secret_name="Tommy Sharp",
            age=48,
            team=team_preventers,
        )
        hero_spider_boy = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
        hero_dummy = Hero(name="Dummy", secret_name="Dummy", age=1, team=team_z_force)
        session.add(hero_deadpond)
        session.add(hero_rusty_man)
        session.add(hero_spider_boy)
        session.add(hero_dummy)
        session.commit()

        session.refresh(hero_deadpond)
        session.refresh(hero_rusty_man)
        session.refresh(hero_spider_boy)

        print("Created hero:", hero_deadpond)
        print("Created hero:", hero_rusty_man)
        print("Created hero:", hero_spider_boy)


def add_hero_to_team():
    with Session(engine) as session:
        statement = select(Team).where(Team.name == "Preventers")
        team_preventers = session.exec(statement).one()

        statement = select(Hero).where(Hero.name == "Spider-Boy")
        hero = session.exec(statement).one()

        team_preventers.heroes.append(hero)
        session.add(team_preventers)
        session.commit()

        session.refresh(team_preventers)
        print("Team Preventers:", team_preventers.heroes)


def main():
    print()
    print("Create DB and tables")
    print("====================")
    print()
    create_db_and_tables()

    print()
    print("Create Heroes")
    print("=============")
    print()
    create_heroes()

    print()
    print("Add Hero to Team")
    print("================")
    print()
    add_hero_to_team()


if __name__ == "__main__":
    main()
