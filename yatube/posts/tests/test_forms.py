from django.test import Client, TestCase
from django.urls import reverse
from posts.forms import PostForm
from posts.models import Group, Post, User


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаем неавторизованный клиент
        cls.guest_client = Client()
        # Создаем авторизованый клиент
        cls.user = User.objects.create_user(username='user')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        # Создадим группу в БД
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Описание группы'
        )
        # Создадим пост в БД
        cls.post = Post.objects.create(
            text='Тестовая запись',
            author=cls.user,
            group=cls.group
        )
        cls.form = PostForm()

    def test_create_post(self):
        """Валидная форма создает запись"""
        # Подсчитаем количество записей
        posts_count = Post.objects.count()
        # Подготавливаем данные для передачи в форму
        form_data = {
            'text': 'Тестовый текст',
            'group': self.group.pk,
            'author': self.user
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        # Проверяем, сработал ли редирект
        self.assertRedirects(response, reverse(
            'posts:profile', kwargs={'username': PostCreateFormTests.user})
        )
        # Проверяем, увеличилось ли число постов
        self.assertEqual(Post.objects.count(), posts_count + 1)
        # Проверяем, что создалась запись с нашим слагом
        last_obj = Post.objects.all().latest('pk')
        self.assertEqual(last_obj.author, form_data['author'])
        self.assertEqual(last_obj.text, form_data['text'])
        self.assertEqual(last_obj.group.pk, form_data['group'])

    def test_authorized_edit_post(self):
        """Редактирование записи создателем поста"""
        # Проверяем, что авторизованный пользователь
        # может редактировать пост
        form_data = {
            'text': 'Тестовый текст',
            'group': self.group.pk,
        }
        self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True,
        )
        post_edit = Post.objects.get(pk=self.group.pk)
        self.client.get(f'/posts/{post_edit.pk}/edit/')
        form_data = {
            'text': 'Измененный текст поста',
            'group': self.group.pk
        }
        response_edit = self.authorized_client.post(
            reverse('posts:post_edit',
                    kwargs={
                        'post_id': post_edit.pk
                    }),
            data=form_data,
            follow=True,
        )
        post_edit = Post.objects.get(pk=self.group.pk)
        self.assertEqual(response_edit.status_code, 200)
        self.assertEqual(post_edit.text, 'Измененный текст поста')
        # Проверка редиректа на страницу поста
        self.assertRedirects(response_edit, reverse(
            'posts:post_detail', kwargs={'post_id': self.post.pk}))
