from django.contrib import admin

from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from user_app.models import Person, ValidRoom, History

# Register your models here.
#
# admin.site.register(Item)
# admin.site.register(ItemPrice)
# admin.site.register(Basket)
# admin.site.register(BasketItem)


class PersonInline(admin.StackedInline):
    model = Person
    can_delete = False
    verbose_name_plural = 'people'


class PersonAdmin(BaseUserAdmin):
    inlines = (PersonInline,)


admin.site.unregister(User)
admin.site.register(User, PersonAdmin)
admin.site.register(ValidRoom)
admin.site.register(History)