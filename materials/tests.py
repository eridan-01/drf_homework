from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User
from .models import Course, Lesson, Subscription


class LessonTestCase(APITestCase):
    def setUp(self):
        # Создание пользователя
        self.user = User.objects.create(
            email='testuser@example.com',
            password='123qwe'
        )

        # Создание курса
        self.course = Course.objects.create(
            title='Тестовый курс',
            description='Описание тестового курса',
            owner=self.user
        )

        # Создание урока
        self.lesson = Lesson.objects.create(
            title='Тестовый урок',
            description='Описание тестового урока',
            course=self.course,
            owner=self.user
        )

        # Аутентификация клиента
        self.client.force_authenticate(user=self.user)

    def test_create_lesson(self):
        """ Тест на создание урока """
        url = reverse('materials:lesson-create')
        data = {
            'title': 'Новый урок',
            'description': 'Описание нового урока',
            'course': self.course.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)
        self.assertEqual(Lesson.objects.get(pk=response.data['id']).title, 'Новый урок')

    def test_list_lessons(self):
        """ Тест на просмотр урока """
        url = reverse('materials:lesson-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Тестовый урок')

    def test_retrieve_lesson(self):
        """ Тест на получение урока """
        url = reverse('materials:lesson-get', args=(self.lesson.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Тестовый урок')

    def test_update_lesson(self):
        """ Тест на изменение урока """
        url = reverse('materials:lesson-update', args=(self.lesson.pk,))
        data = {
            'title': 'Измененный урок',
            'description': 'Описание измененного урока',
            'course': self.course.id
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, 'Измененный урок')

    def test_delete_lesson(self):
        """ Тест на удаление урока """
        url = reverse('materials:lesson-delete', args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        # Создание пользователя
        self.user = User.objects.create(
            email='testuser@example.com',
            password='123qwe'
        )

        # Создание курса
        self.course = Course.objects.create(
            title='Тестовый курс',
            description='Описание тестового курса',
            owner=self.user
        )

        # Аутентификация клиента
        self.client.force_authenticate(user=self.user)

    def test_subscription_activate(self):
        """Тест подписки на курс"""
        url = reverse('materials:subscribe')
        data = {
            "user": self.user.id,
            "course_id": self.course.id,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "message": "Подписка добавлена",
            },
        )
        self.assertTrue(
            Subscription.objects.all().exists(),
        )

    def test_subscription_deactivate(self):
        """Тест отписки с курса"""
        url = reverse('materials:subscribe')
        Subscription.objects.create(
            user=self.user,
            course=self.course)
        data = {
            "user": self.user.id,
            "course_id": self.course.id,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.json(),
            {
                "message": "Подписка удалена",
            },
        )
        self.assertFalse(
            Subscription.objects.all().exists(),
        )