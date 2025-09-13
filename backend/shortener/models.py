from django.db import models

class Link(models.Model):
    code = models.CharField(max_length=10, unique=True, db_index=True)
    long_url = models.TextField()
    clicks = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.code} -> {self.long_url}"
