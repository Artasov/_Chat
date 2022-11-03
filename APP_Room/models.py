from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify


class Room(models.Model):
    name = models.CharField(unique=True, max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)
    users = models.ManyToManyField(User, related_name='room_users', blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Room, self).save(*args, **kwargs)


class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def as_json(self):
        return dict(
            room=self.room.name,
            user=self.user.username,
            content=self.content,
            date_added=self.date_added.isoformat()
        )

    class Meta:
        ordering = ('date_added',)