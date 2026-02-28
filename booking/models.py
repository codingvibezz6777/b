from django.db import models
from django.utils.text import slugify



class Celebrity(models.Model):
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar ($)'),
        ('EUR', 'Euro (€)'),
        ('GBP', 'British Pound (£)'),
        ('AUD', 'Australian Dollar (A$)'),
        ('CAD', 'Canadian Dollar (C$)'),
        ('JPY', 'Japanese Yen (¥)'),
        ('CNY', 'Chinese Yuan (¥)'),
        ('INR', 'Indian Rupee (₹)'),
    ]
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='celebrities/')
    instagram = models.URLField(max_length=500, blank=True, null=True)
    tweeter = models.URLField(max_length=500, blank=True, null=True)
    fbk = models.URLField(max_length=500, blank=True, null=True)
    youtube = models.URLField(max_length=500, blank=True, null=True)
    category = models.CharField(max_length=100)
    bio = models.TextField(default="", blank=True)
    extra = models.TextField(default="", blank=True)
    price_range = models.CharField(max_length=100)
    stagename = models.CharField(max_length=100,blank=True,
    null=True)
    currency = models.CharField(
        max_length=20,
        choices=CURRENCY_CHOICES,
        default='USD'
    )
    available = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Celebrity.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)
        
        if self.instagram and not self.instagram.startswith(('http://', 'https://')):
            self.instagram = 'https://' + self.instagram
        
        if self.tweeter and not self.tweeter.startswith(('http://', 'https://')):
            self.tweeter = 'https://' + self.tweeter
        
        if self.fbk and not self.fbk.startswith(('http://', 'https://')):
            self.fbk = 'https://' + self.fbk
        
        if self.youtube and not self.youtube.startswith(('http://', 'https://')):
            self.youtube = 'https://' + self.youtube
        
        super().save(*args, **kwargs)

    

class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    EVENT_CHOICES = (
        ('Birthday', 'Birthday'),
        ('Meet and Greet', 'Meet and Greet'),
        ('Convention/Tradeshow', 'Convention/Tradeshow'),
        ('Cooking demo', 'Cooking demo'),
        ('Endorsement/Spokeperson','Endorsement/Spokeperson'),
        ('Funeral', 'Funeral'),
        ('Musical Perfomance','Musical Perfomance'),
        ('Personal Appearance','Personal Appearance'),
        ('Satelite Media Tour', 'Satelite Media Tour'),
        ('Speaking Engagement', 'Speaking Engagement'),
        ('Virtual Event', 'Virtual Event'),
        ('Weddings', 'Weddings'),
    )
    
    BUDGET_CHOICES = (
        ('$5,000 - or less', '$5,000- or less'),
        ('$5,000 - $10,000', '$5,000 - $10,000'),
        ('$10,000 - $20,000', '$10,000 - $20,000'),
        ('$20,000 - $30,000', '$20,000 - $30,000'),
        ('$50,000 - $100,000','$50,000 - $100,000'),
        ('$100,000 - or more', '$100,000 - or more'),
    )
    celebrity = models.ForeignKey(Celebrity, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    event_type = models.CharField(max_length=100,choices=EVENT_CHOICES,default='Meet and Greet')
    event_location = models.CharField(max_length=150, blank=True)
    event_date = models.DateField()
    budget = models.CharField(max_length=50,choices=BUDGET_CHOICES,default='$5,000 - or less')
    airport = models.CharField(max_length=100,blank=True,
    null=True)
    addinfo = models.TextField(max_length=100,blank=True,
    null=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} booked {self.celebrity.name}"
