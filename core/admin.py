from django.contrib import admin
from django.http import HttpResponse
import csv
from .models import CodeSession, BugReport, Feedback


def export_feedback_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="feedback.csv"'
    writer = csv.writer(response)
    writer.writerow([
        'Feedback ID', 'User', 'Bug ID', 'Bug Type',
        'Line Number', 'Description', 'Fix Suggestion',
        'Verdict', 'Language', 'Created At'
    ])
    for fb in queryset:
        writer.writerow([
            fb.id,
            fb.user.username,
            fb.bug_report.id,
            fb.bug_report.bug_type,
            fb.bug_report.line_number,
            fb.bug_report.description,
            fb.bug_report.fix_suggestion,
            fb.verdict,
            fb.bug_report.session.language,
            fb.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        ])
    return response

export_feedback_csv.short_description = 'Export selected feedback as CSV'


@admin.register(CodeSession)
class CodeSessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'language', 'risk_level', 'error_count', 'created_at']
    list_filter = ['language', 'risk_level', 'created_at']
    search_fields = ['user__username', 'code']
    readonly_fields = ['created_at']
    ordering = ['-created_at']


@admin.register(BugReport)
class BugReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'session', 'bug_type', 'line_number', 'created_at']
    list_filter = ['bug_type']
    search_fields = ['description', 'fix_suggestion']
    readonly_fields = ['created_at']
    ordering = ['-created_at']


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'bug_report', 'verdict', 'created_at']
    list_filter = ['verdict', 'created_at']
    search_fields = ['user__username']
    readonly_fields = ['created_at']
    actions = [export_feedback_csv]
    ordering = ['-created_at']