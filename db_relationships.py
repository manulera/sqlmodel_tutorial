from typing import Optional
from sqlmodel import Field, SQLModel, create_engine, Session, select, or_
import os

if os.path.exists("database_rel.db"):
    os.remove("database_rel.db")


class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # index=True is used to create an index on the column
    # this makes the column faster to search
    # but slower to write
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)

    team_id: Optional[int] = Field(default=None, foreign_key="team.id")


sqlite_file_name = "database_rel.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_heroes():
    with Session(engine) as session:
        team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
        team_z_force = Team(name="Z-Force", headquarters="Sister Margaret's Bar")
        session.add(team_preventers)
        session.add(team_z_force)
        session.commit()

        hero_deadpond = Hero(
            name="Deadpond", secret_name="Dive Wilson", team_id=team_z_force.id
        )
        hero_rusty_man = Hero(
            name="Rusty-Man",
            secret_name="Tommy Sharp",
            age=48,
            team_id=team_preventers.id,
        )
        hero_spider_boy = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
        hero_dummy = Hero(
            name="Dummy", secret_name="Dummy", age=1, team_id=team_z_force.id
        )
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


def do_joins():

    with Session(engine) as session:
        # First syntax
        statement = select(Hero, Team).where(Hero.team_id == Team.id)
        results = session.exec(statement)
        for hero, team in results:
            print("Hero:", hero, "Team:", team)

        # Alt syntax using join
        statement = select(Hero, Team).join(Team)
        results = session.exec(statement)
        for hero, team in results:
            print("Hero:", hero, "Team:", team)

        # Left outer join (include heroes without a team)
        statement = select(Hero, Team).join(Team, isouter=True)
        results = session.exec(statement)
        for hero, team in results:
            print("Hero:", hero, "Team:", team)

        # You can use a join to filter by a related class attribute,
        # for example, to get all heroes that are in the Preventers team,
        # even if you don't include Team in the select
        statement = select(Hero).join(Team).where(Team.name == "Preventers")
        results = session.exec(statement)
        for hero in results:
            print("Hero:", hero)


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
    print("Do Joins")
    print("========")
    print()
    do_joins()


if __name__ == "__main__":
    main()
