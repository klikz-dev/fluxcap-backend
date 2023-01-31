from settings.models import Point, Site, Tag, Zone
from settings.forms import SiteForm
from django.contrib import admin


class SiteAdmin(admin.ModelAdmin):
    form = SiteForm

    fieldsets = [
        ('Credentials', {'fields': ['hostname',
         'port', 'username', 'password', 'topic']}),
        ('Floor Configuration', {'fields': ['floor_image', 'floor_width', 'floor_height',
         'floor_x', 'floor_y', 'floor_border_x', 'floor_border_y', 'floor_ratio']}),
        ('Additional Settings', {'fields': ['alert_threshold', ]}),
    ]

    list_display = ('hostname', 'port', 'username', 'topic')

    search_fields = ['hostname', 'port', 'username', 'topic']


class TagAdmin(admin.ModelAdmin):
    fields = ['tag_id', 'label', 'color', 'x', 'y', 'z',
              'latency', 'success', 'update', 'loss', 'blink_index', 'site']

    list_display = ('tag_id', 'label', 'color', 'x',
                    'y', 'z', 'first_seen', 'last_seen', 'site')

    search_fields = ['tag_id', 'label', 'color']


class PointInline(admin.TabularInline):
    model = Point
    extra = 0
    min = 3

    fields = ['x', 'y']


class ZoneAdmin(admin.ModelAdmin):
    fields = ['zone_id', 'label', 'color', 'site']

    list_display = ('zone_id', 'label', 'color', 'site')

    search_fields = ['label']

    inlines = [PointInline]


class PointAdmin(admin.ModelAdmin):
    fields = ['x', 'y', 'zone']

    list_display = ('x', 'y', 'zone')

    search_fields = ['x', 'y']


admin.site.register(Site, SiteAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Zone, ZoneAdmin)
admin.site.register(Point, PointAdmin)
