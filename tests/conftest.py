from uuid import uuid4

import pytest
from sqlalchemy import Column, create_engine, MetaData, StaticPool, String, Table
from sqlalchemy.orm import sessionmaker

from sqlalchemy_guid.guid import GUID


@pytest.fixture(scope='session', autouse=True)
def engine():
    return create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )


@pytest.fixture(scope='session', autouse=True)
def session(engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def students_table(engine):
    metadata = MetaData()
    metadata.drop_all(engine)

    students_table = Table(
        'students', metadata,
        Column('id', GUID, primary_key=True),
        Column('firstname', String),
        Column('lastname', String),
    )
    metadata.create_all(engine)

    yield students_table

    metadata.drop_all(engine)


@pytest.fixture
def create_one_student(session, students_table, faker):
    student = {
        'id': uuid4(),
        'firstname': faker.first_name(),
        'lastname': faker.last_name(),
    }
    query = students_table.insert().values(student)

    with session() as s:
        s.execute(query)
        s.commit()

    return student


@pytest.fixture
def create_many_students(session, students_table, faker):
    students = [
        {
            'id': uuid4(),
            'firstname': faker.first_name(),
            'lastname': faker.last_name(),
        }
        for _ in range(5)
    ]

    query = students_table.insert().values(students)

    with session() as s:
        s.execute(query)
        s.commit()

    return students
