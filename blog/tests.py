from django.test import TestCase
from django.test import SimpleTestCase
from .models import Blog
from django.urls import reverse
# Create your tests here.

class PagesTests(TestCase):
    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_by_name(self):
        resp = self.client.get(reverse('homepage'))
        self.assertEqual(resp.status_code, 200)
    
    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('homepage'))
        self.assertTemplateUsed(resp, 'homepage.html')


class BlogModelTest(TestCase):
    def Setup(self):
        Blog.objects.Create(text='test tedfght')
    
    def test_text_content(self):
        blog = Blog.objects.get(id=2)
        expected_object_name = f'{blog.text}'
        self.assertEqual(expected_object_name, 'hewlo wortld')


class BlogTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
        username='testuser',
        email='test@email.com',
        password='secret'
        )
        self.blog = Blog.objects.create(
        title='A good title',
        body='Nice body content',
        author=self.user,
        )

    def test_string_representation(self):
        Blog = Blog(title='A sample title')
        self.assertEqual(str(blog), blog.title)
        def test_blog_content(self):
        self.assertEqual(f'{self.blog.title}', 'A good title')
        self.assertEqual(f'{self.blog.author}', 'testuser')
        self.assertEqual(f'{self.blog.body}', 'Nice body content')
        def test_blog_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response. .status_code, 200)
        self.assertContains(response, 'Nice body content')
        self.assertTemplateUsed(response, 'home.html')

    def test_blog_detail_view(self):
        response = self. .client. .get('/blog/1/')
        no_response = self.client.get('/blog/100000/')
        self.assertEqual(response. .status_code, 200)
        self.assertEqual(no_response. .status_code, 404)
        self.assertContains(response, 'A good title')
        self.assertTemplateUsed(response, 'blog_detail.html')