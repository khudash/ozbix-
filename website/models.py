from django.db import models

class Banner(models.Model):
    image = models.ImageField(upload_to="banner/")

    def __str__(self):
        return str(self.image)


# 
class Service(models.Model):
    icon_class = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    short_description = models.CharField(max_length=150)
    description = models.TextField()
    button_text = models.CharField(max_length=50, default="Read More")

    def __str__(self):
        return self.title


    
# 
class OzbixFolio(models.Model):
    image = models.ImageField(upload_to="ozbixfolio/")
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    

# 
class Client(models.Model):
    image = models.ImageField(upload_to="clients/")

    def __str__(self):
        return "Client Image"