from django.db import models
from django.contrib.auth.models import User


class CodeSession(models.Model):
    LANGUAGE_CHOICES = [
        ('python', 'Python'),
        ('java', 'Java'),
        ('c', 'C'),
        ('cpp', 'C++'),
    ]

    RISK_CHOICES = [
        ('safe', 'Safe'),
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES)
    code = models.TextField()
    risk_level = models.CharField(max_length=10, choices=RISK_CHOICES, default='safe')
    error_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.language} - {self.created_at.strftime('%d %b %Y')}"


class BugReport(models.Model):
    BUG_TYPE_CHOICES = [
        ('syntax', 'Syntax Error'),
        ('logical', 'Logical Error'),
        ('runtime', 'Runtime Error'),
        ('warning', 'Warning'),
        ('style', 'Style Issue'),
    ]

    session = models.ForeignKey(CodeSession, on_delete=models.CASCADE, related_name='bugs')
    line_number = models.IntegerField()
    bug_type = models.CharField(max_length=20, choices=BUG_TYPE_CHOICES)
    description = models.TextField()
    fix_suggestion = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bug at line {self.line_number} - {self.bug_type}"


class Feedback(models.Model):
    FEEDBACK_CHOICES = [
        ('correct', 'Correct'),
        ('incorrect', 'Incorrect'),
    ]

    bug_report = models.OneToOneField(BugReport, on_delete=models.CASCADE, related_name='feedback')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    verdict = models.CharField(max_length=10, choices=FEEDBACK_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.verdict} - Bug #{self.bug_report.id}"