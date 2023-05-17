from random import choice
from datacenter.models import Mark
from datacenter.models import Chastisement
from datacenter.models import Schoolkid
from datacenter.models import Commendation
from datacenter.models import Lesson
from datacenter.models import Subject


COMMENDATIONS = [
    'Молодец!',
    'Отлично!',
    'Ты меня приятно удивил!',
    'Уже существенно лучше!',
    'Я поражен!',
    'Ты меня очень обрадовал!',
    'Ты сегодня прыгнул выше головы!',
    'Так держать!',
]


def fix_marks(schoolkid):
    marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])
    for mark in marks:
        points = mark
        points.points = 5
        points.save()


def remove_chastisements(schoolkid):
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    chastisements.delete()


def get_lesson(year_of_study, group_letter, title):
    subject = Subject.objects.get(
        year_of_study=year_of_study,
        title=title,
    )

    lessons = Lesson.objects.filter(
        year_of_study=year_of_study,
        group_letter=group_letter,
        subject=subject,
        )
    lessons = lessons.order_by('date')
    return lessons.first()


def create_commendation(full_name, subject):
    text = choice(COMMENDATIONS)
    try:
        child = Schoolkid.objects.get(full_name__contains=full_name)
        lesson = get_lesson(child.year_of_study, child.group_letter, subject)
    except Schoolkid.DoesNotExist:
        print('Ученика с таким именем не найдено, проверьте правильность написания имени.')
        return
    except Subject.DoesNotExist:
        print('В названии предмета допущена ошибка, либо такого предмета не существует.')
        return
    except Schoolkid.MultipleObjectsReturned:
        print('Найдено больше одного ученика с таким именем, попробуйте указать полное имя(ФИО)')
        return
    commendation = Commendation.objects.create(
        text=text,
        schoolkid=child,
        created=lesson.date,
        subject=lesson.subject,
        teacher=lesson.teacher,
        )
    return commendation
