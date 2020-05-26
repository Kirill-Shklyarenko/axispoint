from django.db import models


# Create your models here.
class Letters(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True,
                                          blank=False)  # Values from 0 to 32767
    category = models.CharField(max_length=15,
                                null=True,
                                blank=False)
    sender = models.CharField(max_length=25,
                              null=True,
                              blank=False)
    title = models.CharField(max_length=100,
                             null=True,
                             blank=False)
    text = models.TextField(null=True,
                            blank=False)
    date = models.DateField(auto_now=False,
                            auto_now_add=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Greeting'
