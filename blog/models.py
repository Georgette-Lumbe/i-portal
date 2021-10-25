from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Models

STATUS = ((0, "Draft"), (1, "Published"))


class Post(models.Model):
    """
    Post database structure
    """
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    featured_image = CloudinaryField('image', default='placeholder')
    excerpt = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(
        User, related_name='post_like', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        """
        Order  our posts on the created_on field
        using descending order
        """
        ordering = ["-created_on"]

    def number_of_likes(self):
        """
        Return total likes of a post
        """
        return self.likes.count()


class Comment(models.Model):
    """
    Comment database structure
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name="comments")
    name = models.CharField(max_length=90)
    email = models.EmailField()
    created_on = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Comment {self.body} by {self.name}"

    class Meta:
        """
        Order  our posts on the created_on field
        """
        ordering = ["created_on"]
