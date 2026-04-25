from .models import History
from django.contrib import admin
from .models import *


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "course",
        "prediction",
        "grade",
        "pass_or_fail",
        "created_at"
    )

    readonly_fields = (
        "user",
        "course",
        "prediction",
        "grade",
        "pass_or_fail",
        "created_at"
    )

    list_filter = ("grade", "pass_or_fail", "course")
    search_fields = ("user__username", "course")

    ordering = ("-created_at",)
