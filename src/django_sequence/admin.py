from django.contrib import admin

# import models
from django_sequence.models import (StageState, StageResult, Sequence, Stage)


class StageResultAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    search_fields = ["name", "description"]


class StageStateAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    search_fields = ["name", "description"]


class SequenceAdmin(admin.ModelAdmin):
    list_display = ("id", "is_complete", "created_at", "updated_at")


class StageAdmin(admin.ModelAdmin):
    list_display = ("id", "sequence", "name", "order", "state", "result", "created_at", "updated_at")
    search_fields = ["sequence", "name", "description"]
    list_filter = ["result", "state", "blocking"]


admin.site.register(StageResult, StageResultAdmin)
admin.site.register(StageState, StageStateAdmin)
admin.site.register(Sequence, SequenceAdmin)
admin.site.register(Stage, StageAdmin)
