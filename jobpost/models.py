from django.db import models
from authentication.models import User
from config.models import BaseModel

# Create your views here.
class JobPost(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=5000)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    attach_file = models.ImageField(upload_to="attach_file/", null=True, blank=True)
    
   

    def __str__(self):
        return self.title
