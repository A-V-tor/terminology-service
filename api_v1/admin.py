from django.contrib import admin

from .models import HandBook, HandBookElement, VersionHandBook


class VersionHandBookInline(admin.TabularInline):
    model = VersionHandBook
    extra = 0


class HandBookElementInline(admin.TabularInline):
    model = HandBookElement
    extra = 0


class HandBookAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'uniq_code',
        'title',
        'latest_version',
        'latest_version_date',
    )
    list_filter = (
        'uniq_code',
        'title',
    )
    inlines = [VersionHandBookInline]

    def latest_version(self, obj):
        latest_version = obj.versions.order_by('-version_start_date').first()
        return latest_version.version if latest_version else 'N/A'

    latest_version.short_description = 'Последняя версия'

    def latest_version_date(self, obj):
        latest_version = obj.versions.order_by('-version_start_date').first()
        return latest_version.version_start_date if latest_version else 'N/A'

    latest_version_date.short_description = 'Дата начала действия'


class VersionHandBookAdmin(admin.ModelAdmin):
    list_display = (
        'handbook_uniq_code',
        'handbook_title',
        'version',
        'version_start_date',
    )
    list_filter = (
        'version',
        'version_start_date',
    )
    list_select_related = ('handbook',)
    inlines = [HandBookElementInline]

    def handbook_uniq_code(self, obj):
        return obj.handbook.uniq_code

    handbook_uniq_code.short_description = 'Код справочника'

    def handbook_title(self, obj):
        return obj.handbook.title

    handbook_title.short_description = 'Наименование справочника'

    def handbook_display(self, obj):
        return str(obj.handbook)

    handbook_display.short_description = 'Справочник'


class HandBookElementAdmin(admin.ModelAdmin):
    list_display = ('uniq_code', 'value')
    list_filter = ('uniq_code',)
    list_select_related = ('version_hand_book',)


admin.site.register(HandBook, HandBookAdmin)
admin.site.register(VersionHandBook, VersionHandBookAdmin)
admin.site.register(HandBookElement, HandBookElementAdmin)
