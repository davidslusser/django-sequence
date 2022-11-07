from django.contrib import admin

# import models
from django_sequence.models import (State, Result, Sequence, Stage)


class ResultAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    search_fields = ["name", "description"]


class StateAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    search_fields = ["name", "description"]


class SequenceAdmin(admin.ModelAdmin):
    list_display = ("id", "is_complete", "created_at", "updated_at")


class StageAdmin(admin.ModelAdmin):
    list_display = ("id", "sequence", "name", "order", "state", "result", "created_at", "updated_at")
    search_fields = ["sequence", "name", "description"]
    list_filter = ["result", "state", "blocking"]


admin.site.register(Result, ResultAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(Sequence, SequenceAdmin)
admin.site.register(Stage, StageAdmin)
