from django.db import models

# Create your models here.
class Codefile(models.Model):
    name=models.CharField(max_length=50)
    code=models.TextField()
    
    def __str__(self):
        return self.name
    