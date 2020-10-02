from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.crypto import get_random_string


class Person(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    number = models.SlugField(max_length=8, blank=True)


def save_number(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        person_profile = Person(user=user)
        person_profile.number = get_random_string(8, '0123456789')
        number_in_use = True
        while number_in_use:
            number_in_use = False
            other_numbers = type(person_profile).objects.filter(number=person_profile.number)
            if len(other_numbers) > 0:
                number_in_use = True
            if number_in_use:
                person_profile.number = get_random_string(8, '0123456789')
        person_profile.save()


post_save.connect(save_number, sender=User)


class ValidRoom(models.Model):
    room_uuid = models.SlugField(blank=True)
    caller1 = models.SlugField(max_length=8, blank=True)
    caller2 = models.SlugField(max_length=8, blank=True)
    validation_username = models.SlugField(max_length=50, blank=True)
    validation_token = models.SlugField(max_length=32, blank=True)
    date = models.DateTimeField(auto_now_add=True)


class History(models.Model):
    caller1 = models.SlugField(max_length=8, blank=True)
    caller2 = models.SlugField(max_length=8, blank=True)
    date = models.DateTimeField(auto_now_add=True)

# # Create your models here.
#
# PLATFORMS = [('', ''), ('PS3', 'PlayStation 3'), ('PS4', 'PlayStation 4'), ('PSV', 'PlayStation Vita'),
#              ('PSP', 'PlayStation Portable'), ('PS2', 'PlayStation 2'), ]
#
#
# class Item(models.Model):
#     item_id = models.AutoField(primary_key=True)
#     title = models.SlugField(blank=False)
#     price = models.FloatField(null=True)
#     platform = models.CharField(max_length=3, choices=PLATFORMS, default=' ')
#     ps_id = models.CharField(max_length=50, blank=True)
#     image = models.SlugField(blank=True)
#     age_rating = models.IntegerField(default=99)
#     trailer_url = models.SlugField(blank=True)
#     onsale = models.BooleanField(default=False)
#     tag = models.SlugField(null=True, blank=True)
#     description = models.TextField(blank=True, null=True)
#
#     def __str__(self):
#         return self.title
#
#
# class ItemPrice(models.Model):
#     item_id = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
#     historical_price = models.FloatField(null=True)
#     date_fetched = models.DateTimeField(auto_now_add=True)
#
#
# #
# # class Basket(models.Model):
# #     basket_title = models.CharField(max_length=100, blank=True, null=True)
# #     basket_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
# #     total = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
#
#
# class BasketItem(models.Model):
#     user_id = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
#     item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
#
#
# class Carousel(models.Model):
#     image_url = models.SlugField()
