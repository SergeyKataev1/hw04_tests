from django.test import TestCase
from posts.models import Group, Post, User


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост длинной больше 15-ти символов',
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        number_of_characters = 15
        post = PostModelTest.post
        text = post.text[:number_of_characters]
        self.assertEqual(str(post), text)
        group = PostModelTest.group
        self.assertEqual(str(group), group.title)
