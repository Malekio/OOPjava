from django.db import models


class Wilaya(models.Model):
    """
    Algerian administrative divisions (wilayas)
    """

    code = models.CharField(max_length=2, unique=True)
    name_ar = models.CharField(max_length=100)  # Arabic name
    name_en = models.CharField(max_length=100)  # English name
    name_fr = models.CharField(max_length=100)  # French name
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "wilayas"
        ordering = ["code"]
        indexes = [
            models.Index(fields=["code"]),
            models.Index(fields=["name_en"]),
        ]

    def __str__(self):
        return f"{self.code} - {self.name_en}"
