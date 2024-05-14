from typing import Optional
from sqlmodel import Field, SQLModel, create_engine, Session, select, or_
import os

if os.path.exists("database.db"):
    os.remove("database.db")


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # index=True is used to create an index on the column
    # this makes the column faster to search
    # but slower to write
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = None


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_heroes():
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
    hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)

    with Session(engine) as session:

        session.add(hero_1)
        session.add(hero_2)
        session.add(hero_3)

        session.commit()

        print("Hero 1 name:", hero_1.name)
        print()
        print("Hero 2 name:", hero_2.name)
        print()
        session.refresh(hero_1)
        print("Hero 1:", hero_1)


def select_heroes():
    with Session(engine) as session:
        statement = select(Hero)
        heroes_iterable = session.exec(statement)

        for hero in heroes_iterable:
            print("Hero:", hero)

        # To get a list:
        heroes_iterable = session.exec(statement)
        heroes_list = heroes_iterable.all()


def add_more_heroes():
    hero_4 = Hero(name="Tarantula", secret_name="Natalia Roman-on", age=32)
    hero_5 = Hero(name="Black Lion", secret_name="Trevor Challa", age=35)
    hero_6 = Hero(name="Dr. Weird", secret_name="Steve Weird", age=36)
    hero_7 = Hero(name="Captain North America", secret_name="Esteban Rogelios", age=93)

    with Session(engine) as session:
        session.add(hero_4)
        session.add(hero_5)
        session.add(hero_6)
        session.add(hero_7)
        session.commit()

        session.refresh(hero_4)
        print("Hero 4:", hero_4)


def filter_heroes():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Deadpond")
        heroes_iterable = session.exec(statement)

        for hero in heroes_iterable:
            print("Hero:", hero)

        # AND statement
        statement = select(Hero).where(Hero.age > 30).where(Hero.age < 40)
        heroes_iterable = session.exec(statement)

        for hero in heroes_iterable:
            print("Hero:", hero)

        # OR statement
        statement = select(Hero).where(or_(Hero.age <= 30, Hero.age >= 40))
        heroes_iterable = session.exec(statement)

        for hero in heroes_iterable:
            print("Hero:", hero)


def more_filtering():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Deadpond")
        heroes_iterable = session.exec(statement)
        # This gives you the first
        picked_hero = heroes_iterable.first()
        print("Hero:", picked_hero)

        statement = select(Hero).where(or_(Hero.age > 30))
        heroes_iterable = session.exec(statement)
        # This will give an error if more than one row is returned
        try:
            picked_hero = heroes_iterable.one()
        except Exception as e:
            print("Error because more than one", e)

        # This will give an error if no row is returned
        statement = select(Hero).where(Hero.name == "Ironman")
        heroes_iterable = session.exec(statement)

        try:
            picked_hero = heroes_iterable.one()
        except Exception as e:
            print("Error because no row", e)

        # Get by id
        hero = session.get(Hero, 1)
        print("Hero:", hero)


def using_limit():
    with Session(engine) as session:
        statement = select(Hero).limit(2)
        heroes_iterable = session.exec(statement)

        for hero in heroes_iterable:
            print("Hero:", hero)

        print("the next 2")

        statement = select(Hero).offset(2).limit(2)
        heroes_iterable = session.exec(statement)

        for hero in heroes_iterable:
            print("Hero:", hero)


def update_hero():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Deadpond")
        heroes_iterable = session.exec(statement)
        picked_hero = heroes_iterable.one()
        picked_hero.name = "Deadpool"
        session.add(picked_hero)
        session.commit()

        statement = select(Hero).where(Hero.name == "Deadpool")
        heroes_iterable = session.exec(statement)
        picked_hero = heroes_iterable.first()
        print("Hero:", picked_hero)


def delete_hero():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Deadpool")
        heroes_iterable = session.exec(statement)
        picked_hero = heroes_iterable.one()
        session.delete(picked_hero)
        session.commit()

        statement = select(Hero).where(Hero.name == "Deadpool")
        heroes_iterable = session.exec(statement)
        picked_hero = heroes_iterable.first()
        print("Hero:", picked_hero)


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
    print("Select Heroes")
    print("=============")
    print()
    select_heroes()
    print()
    print("Add more Heroes")
    print("=============")
    print()
    add_more_heroes()
    print()
    print("Filter Heroes")
    print("=============")
    print()
    filter_heroes()
    print()
    print("More filtering")
    print("=============")
    print()
    more_filtering()
    print()
    print("Using limit")
    print("=============")
    print()
    using_limit()
    print()
    print("Update Hero")
    print("=============")
    print()
    update_hero()
    print()
    print("Delete Hero")
    print("=============")
    print()
    delete_hero()
    print()


if __name__ == "__main__":
    main()
