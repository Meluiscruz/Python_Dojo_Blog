from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import Post

class BlogTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username = 'bojack_horseman',
            email = 'bojack@meluiscruz.com',
            password = 'Aive3aed',
        )

        self.post = Post.objects.create(
            title = 'This is a test',
            body = '''Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                Morbi ut odio varius mi dignissim placerat. 
                Duis aliquet nec dui vitae gravida.''',
            author = self.user
        )
    
    def test_string_representation(self):
        post = Post(title='This is a test')
        self.assertEqual(str(post),post.title)
    
    def test_post_content(self):
        self.assertEqual(f'{self.post.title}', 'This is a test')
        self.assertEqual(f'{self.post.author}', 'bojack_horseman')
        self.assertEqual(f'{self.post.body}', '''Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                Morbi ut odio varius mi dignissim placerat. 
                Duis aliquet nec dui vitae gravida.''')
    
    def test_post_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '''Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                Morbi ut odio varius mi dignissim placerat. 
                Duis aliquet nec dui vitae gravida.''')
        self.assertTemplateUsed(response, 'home.html')
    
    def test_post_detail_view(self):
        response = self.client.get('/post/1/')
        no_response = self.client.get('/post/800/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, '''Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                Morbi ut odio varius mi dignissim placerat. 
                Duis aliquet nec dui vitae gravida.''')
        self.assertTemplateUsed(response, 'post_detail.html')