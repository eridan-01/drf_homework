from django.db import models

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    name_of_course = models.CharField(
        max_length=100,
        verbose_name="Название курса",
        help_text="Укажите название курса"
    )

    preview = models.ImageField(
        upload_to="materials/courses",
        verbose_name="Изображение (превью)",
        **NULLABLE,
        help_text="Загрузите изображение для превью курса"
    )

    description = models.TextField(
        verbose_name="Описание курса",
        **NULLABLE,
        help_text="Опишите основные материалы курса"
    )

    def __str__(self):
        return f"{self.name_of_course}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название урока",
        help_text="Укажите название урока"
    )

    description = models.TextField(
        verbose_name="Описание урока",
        **NULLABLE,
        help_text="Опишите основные материалы урока"
    )

    preview = models.ImageField(
        upload_to="materials/lessons",
        verbose_name="Изображение (превью)",
        **NULLABLE,
        help_text="Загрузите изображение для превью урока"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name="Курс",
        **NULLABLE,
        related_name="lessons",
    )

    video_url = models.URLField(
        verbose_name="Ссылка на видео",
        **NULLABLE,
        help_text="Укажите ссылку на видео урока",
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

