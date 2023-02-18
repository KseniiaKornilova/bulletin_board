from django.contrib import admin
from .models import AdvUser, SuperRubric, SubRubric, Bb, AdditionalImage
from .utilities import send_activation_notification
from .forms import SubRubricForm



# Register your models here.

def send_activation_notification(modeladmin, request, queryset):
    for rec in queryset:
        if not rec.is_activated:
            send_activation_notification(rec)
    modeladmin.message_user(request, 'Письма с требованиями отправлены')
send_activation_notification.short_description = 'Отправка писем с требованиями активации'


class AdvUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_activated', 'date_joined')
    # list_editable = ('is_activated', )
    ordering = ('username',)
    list_per_page = 5
    search_fields = ('^username', '^email', '^first_name', '^last_name')
    list_filter = ('is_activated',)
    fields = (('username', 'email'), ('first_name', 'last_name'),
    ('send_message', 'is_active', 'is_activated'), 
    ('is_staff', 'is_superuser'), ('groups', 'user_permissions'),
    ('last_login', 'date_joined'))
    readonly_fields = ('last_login', 'date_joined')
    actions = (send_activation_notification,)

admin.site.register(AdvUser, AdvUserAdmin)

class SubRubricInline(admin.TabularInline):
    model = SubRubric

class SuperRubricAdmin(admin.ModelAdmin):
    exclude = ('super_rubric',)
    inlines = (SubRubricInline,)

admin.site.register(SuperRubric, SuperRubricAdmin)


class SubRubricAdmin(admin.ModelAdmin):
    form = SubRubricForm

admin.site.register(SubRubric, SubRubricAdmin)


class AdditionalImageInline(admin.TabularInline):
    model = AdditionalImage

class BbAdmin(admin.ModelAdmin):
    list_display = ('rubric', 'title', 'content', 'author', 'created_at')
    fields = (('rubric', 'author'), 'title', 'content', 'price')
    inlines = (AdditionalImageInline,)

admin.site.register(Bb, BbAdmin)