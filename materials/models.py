from django.db import models

from config.settings import AUTH_USER_MODEL

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Название курса",
        help_text="Укажите название курса",
    )

    preview = models.ImageField(
        upload_to="materials/courses",
        verbose_name="Изображение (превью)",
        **NULLABLE,
        help_text="Загрузите изображение для превью курса",
    )

    description = models.TextField(
        verbose_name="Описание курса",
        **NULLABLE,
        help_text="Опишите основные материалы курса",
    )

    owner = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name="Автор"
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Название урока",
        help_text="Укажите название урока",
    )

    description = models.TextField(
        verbose_name="Описание урока",
        **NULLABLE,
        help_text="Опишите основные материалы урока",
    )

    preview = models.ImageField(
        upload_to="materials/lessons",
        verbose_name="Изображение (превью)",
        **NULLABLE,
        help_text="Загрузите изображение для превью урока",
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

    owner = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name="Автор"
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Subscription(models.Model):
    user = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь"
    )

    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата подписки")

    is_active = models.BooleanField(default=True, verbose_name="Активная подписка")

    def __str__(self):
        return f"{self.user} - {self.course}"

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
