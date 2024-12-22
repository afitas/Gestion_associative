from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Announcement(models.Model):
    title = models.CharField(max_length=255, verbose_name="Titre")
    content = models.TextField(verbose_name="Contenu")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Créé par",
        related_name='announcements'
    )

    class Meta:
        verbose_name = "Annonce"
        verbose_name_plural = "Annonces"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} (créé le {self.created_at.strftime('%d/%m/%Y')})"
