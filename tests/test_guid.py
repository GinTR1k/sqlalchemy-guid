import uuid


def test_select_one_record(session, students_table, create_one_student):
    with session() as s:
        results = s.execute(students_table.select()).all()

    assert len(results) == 1

    student = results[0]

    assert isinstance(student.id, uuid.UUID)
    assert student.id == create_one_student['id']
    assert student.firstname == create_one_student['firstname']
    assert student.lastname == create_one_student['lastname']


def test_select_with_sort(session, students_table, create_many_students):
    with session() as s:
        results = s.execute(students_table.select().order_by(students_table.c.id.asc())).all()

    assert len(results) == len(create_many_students)

    expected_results = sorted(create_many_students, key=lambda x: x['id'])

    for student, expected_student in zip(results, expected_results):
        assert isinstance(student.id, uuid.UUID)
        assert student.id == expected_student['id']
        assert student.firstname == expected_student['firstname']
        assert student.lastname == expected_student['lastname']


def test_select_with_filter(session, students_table, create_many_students):
    searching_student = create_many_students[1]

    with session() as s:
        results = s.execute(
            students_table.select().where(
                students_table.c.id == searching_student['id']
            )
        ).all()

    assert len(results) == 1

    student = results[0]

    assert isinstance(student.id, uuid.UUID)
    assert student.id == searching_student['id']
    assert student.firstname == searching_student['firstname']
    assert student.lastname == searching_student['lastname']
