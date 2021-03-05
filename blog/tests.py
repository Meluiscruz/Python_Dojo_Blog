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
    
    def test_get_absolute_url(self):
        self.assertEqual(self.post.get_absolute_url(), '/post/1/')

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
    
    def test_post_create_view(self):
        response = self.client.post(reverse('post_new'),{
            'title': 'New Title',
            'body' : 'New irrelevant body',
            'author' : self.user.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, 'New Title')
        self.assertEqual(Post.objects.last().body, 'New irrelevant body')

    def test_post_update_vies(self):
        response = self.client.post(reverse('post_edit', args='1'),
        {
            'title': 'Updated Title',
            'body' : 'Updated body',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, 'Updated Title')
        self.assertEqual(Post.objects.last().body, 'Updated body')

    def test_post_delete_vies(self):
        response = self.client.post(reverse('post_delete', args='1'))
        self.assertEqual(response.status_code, 302)

