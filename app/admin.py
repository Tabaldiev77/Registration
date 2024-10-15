from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


admin.site.register(CustomUser)





























# class CustomUserAdmin(UserAdmin):
#     model = CustomUser
#     # Замените 'username' на 'email' и удалите любые упоминания 'username'
#     list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
#     list_filter = ('is_staff', 'is_active')
#     search_fields = ('email', 'first_name', 'last_name')
#     ordering = ('email',)
#
#     # Укажите правильные поля для создания и редактирования пользователя
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('Personal info', {'fields': ('first_name', 'last_name')}),
#         ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'is_staff', 'is_active')}
#         ),
#     )

