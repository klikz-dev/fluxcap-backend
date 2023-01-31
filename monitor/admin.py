from monitor.models import Alert, Record
from django.contrib import admin


class RecordAdmin(admin.ModelAdmin):
    actions = None

    def get_readonly_fields(self, request, obj=None):
        return self.fields or [f.name for f in self.model._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    fields = ['tag_id', 'x', 'y', 'z', 'label', 'color', 'site']

    list_display = ('tag_id', 'x', 'y', 'z', 'label', 'color', 'time', 'site')

    list_filter = ['tag_id']

    search_fields = ['tag_id']


class AlertAdmin(admin.ModelAdmin):
    actions = None

    def get_readonly_fields(self, request, obj=None):
        return self.fields or [f.name for f in self.model._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    fields = ['tag1_id', 'tag2_id']

    list_display = ('tag1_id', 'tag2_id', 'start', 'end', 'duration', 'threshold')

    search_fields = ['tag1_id', 'tag2_id']


admin.site.register(Record, RecordAdmin)
admin.site.register(Alert, AlertAdmin)
