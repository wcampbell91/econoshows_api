from django.db import models

class ShowBand(models.Model):
    band = models.ForeignKey("Band", on_delete=models.DO_NOTHING, related_name='shows')
    show = models.ForeignKey("Show", on_delete=models.DO_NOTHING, related_name='bands')
