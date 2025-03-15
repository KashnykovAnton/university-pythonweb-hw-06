from sqlalchemy import select, func, desc
from sqlalchemy.orm import Session

from db import SessionLocal
from models import Student, Grade, Subject, Teacher, Group


# 1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
def select_1(session: Session):
    query = (
        select(
            Student.name,
            (func.trunc(func.avg(Grade.grade) * 100) / 100).label("avg_grade"),
        )
        .join(Grade)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .limit(5)
    )
    return session.execute(query).all()


# 2. Знайти студента із найвищим середнім балом з певного предмета.
def select_2(session: Session, subject_id: int):
    stmt = (
        select(Student.name, func.avg(Grade.grade).label("avg_grade"))
        .join(Grade)
        .where(Grade.subject_id == subject_id)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .limit(1)
    )
    return session.execute(stmt).first()


# 3. Знайти середній бал у групах з певного предмета.
def select_3(session: Session, subject_id: int):
    stmt = (
        select(
            Group.name,
            (func.trunc(func.avg(Grade.grade) * 100) / 100).label("avg_grade"),
        )
        .join(Student, Group.id == Student.group_id)
        .join(Grade, Student.id == Grade.student_id)
        .where(Grade.subject_id == subject_id)
        .group_by(Group.id)
    )
    return session.execute(stmt).all()


# 4. Знайти середній бал на потоці (по всій таблиці оцінок).
def select_4(session: Session):
    stmt = select((func.trunc(func.avg(Grade.grade) * 100) / 100).label("avg_grade"))
    return session.execute(stmt).scalar()


# 5. Знайти які курси читає певний викладач.
def select_5(session: Session, teacher_id: int):
    stmt = select(Subject.name).where(Subject.teacher_id == teacher_id)
    return session.execute(stmt).all()


# 6. Знайти список студентів у певній групі.
def select_6(session: Session, group_id: int):
    stmt = select(Student.name).where(Student.group_id == group_id)
    return session.execute(stmt).all()


# 7. Знайти оцінки студентів у окремій групі з певного предмета.
def select_7(session: Session, group_id: int, subject_id: int):
    stmt = (
        select(Student.name, Grade.grade, Grade.date_received)
        .join(Grade, Student.id == Grade.student_id)
        .where(Student.group_id == group_id, Grade.subject_id == subject_id)
    )
    return session.execute(stmt).all()


# 8. Знайти середній бал, який ставить певний викладач зі своїх предметів.
def select_8(session: Session, teacher_id: int):
    stmt = (
        select((func.trunc(func.avg(Grade.grade) * 100) / 100).label("avg_grade"))
        .join(Subject, Grade.subject_id == Subject.id)
        .where(Subject.teacher_id == teacher_id)
    )
    return session.execute(stmt).scalar()


# 9. Знайти список курсів, які відвідує певний студент.
def select_9(session: Session, student_id: int):
    stmt = (
        select(Subject.name)
        .join(Grade, Subject.id == Grade.subject_id)
        .where(Grade.student_id == student_id)
        .distinct()
    )
    return session.execute(stmt).all()


# 10. Список курсів, які певному студенту читає певний викладач.
def select_10(session: Session, student_id: int, teacher_id: int):
    stmt = (
        select(Subject.name)
        .join(Grade, Subject.id == Grade.subject_id)
        .where(Grade.student_id == student_id, Subject.teacher_id == teacher_id)
        .distinct()
    )
    return session.execute(stmt).all()


if __name__ == "__main__":
    session: Session = SessionLocal()

    result_1 = select_1(session)
    result_2 = select_2(session, 1)
    result_3 = select_3(session, 1)
    result_4 = select_4(session)
    result_5 = select_5(session, 1)
    result_6 = select_6(session, 1)
    result_7 = select_7(session, 1, 1)
    result_8 = select_8(session, 1)
    result_9 = select_9(session, 1)
    result_10 = select_10(session, 1, 1)

print("\n1. 5 студентів із найбільшим середнім балом:", result_1, "\n")
print("2. Студент із найвищим середнім балом з предмета 1:", result_2, "\n")
print("3. Середній бал у групах з предмета 1:", result_3, "\n")
print("4. Середній бал на потоці:", result_4, "\n")
print("5. Курси, які читає викладач 1:", result_5, "\n")
print("6. Список студентів у групі 1:", result_6, "\n")
print("7. Оцінки студентів у групі 1 з предмета 1:", result_7, "\n")
print("8. Середній бал викладача 1:", result_8, "\n")
print("9. Курси, які відвідує студент 1:", result_9, "\n")
print("10. Курси, які студенту 1 читає викладач 1:", result_10, "\n")
