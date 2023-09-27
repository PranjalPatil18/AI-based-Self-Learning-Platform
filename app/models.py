from django.db import models

# Create your models here.
class sentences(models.Model):
    qus = models.CharField(max_length=1000)

    def __str__(self):
        return self.qus
    
    
class speech_result(models.Model):
    student_name = models.CharField(max_length=1000)
    para = models.CharField(max_length=1000)
    not_recognized_words = models.CharField(max_length=1000)
    meaning = models.CharField(max_length=100)
    progress = models.CharField(max_length=100)

    def __str__(self):
        return self.student_name