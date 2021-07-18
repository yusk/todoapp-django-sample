from django.contrib import admin
from django.db.models import Model
from django.contrib.admin.sites import AlreadyRegistered
from django.utils.safestring import mark_safe

from main import models
from main.models import User, Task
from main.utils import register_admin, get_field_names, export_as_json

admin.site.add_action(export_as_json, 'export_as_json')


class UserAdmin(admin.ModelAdmin):
    search_fields = ['id', 'name', 'email']
    list_filter = ('is_staff', 'is_superuser')
    ordering = ['-created_at']
    date_hierarchy = 'created_at'

    def get_list_display(self, request):
        list_display = get_field_names(User)
        list_display.append("image_show")
        return list_display

    @mark_safe
    def image_show(self, row):
        if row.icon:
            return f'<img src="{row.icon.url}" style="width:100px;height:auto;">'
        return ""


class TaskAdmin(admin.ModelAdmin):
    list_display = get_field_names(Task)
    # list_editable = ['is_done']
    # list_filter = ('is_done', )
    list_per_page = 100
    # list_select_related = ('child_tasks', )
    search_fields = ['title']
    filter_horizontal = ('child_tasks', )
    ordering = None
    empty_value_display = '-'
    date_hierarchy = 'created_at'

    # def view_tags(self, obj):
    #     return ",".join([tag.name for tag in obj.get_all_tags()])

    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        # list_display.extend(["view_tags", "get_tag_count", "get_tag_added_at"])
        return list_display


admin.site.register(User, UserAdmin)
admin.site.register(Task, TaskAdmin)

# 残りのモデルを全て登録
for name in dir(models):
    obj = getattr(models, name)
    if not isinstance(obj, type):
        continue

    if issubclass(getattr(models, name), Model):
        try:
            register_admin(obj)
        except AlreadyRegistered:
            pass
