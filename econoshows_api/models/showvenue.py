from django.db import models

class ShowVenue(models.Model):
    venue = models.ForeignKey("Venue", on_delete=models.DO_NOTHING, related_name="shows")
    show = models.ForeignKey("Show", on_delete=models.DO_NOTHING, related_name="venue")
