from django.db import models
from datetime import date
from django.urls import reverse


# Create your models here.
class Picture(models.Model):
    title = models.CharField('标题',max_length=100,blank=True,default='')
    image = models.ImageField('图片',upload_to='mypicture',blank=True)
    date = models.DateField(default=date.today)

    def get_absolute_url(self):
        return reverse('pic_upload:pic_detail', args=[str(self.id)])

