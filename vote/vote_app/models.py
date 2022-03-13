from django.db import models

class TelegramUser(models.Model):
    telegram_id = models.CharField('Telegram ID', max_length=355)
    name = models.CharField('Telegram Name', max_length=355)
    phone_number = models.CharField('Phone Number', max_length=355)
    username = models.CharField('Username', max_length=355)

    def __str__(self):
        return self.name


class Title(models.Model):
    title = models.CharField('Title', max_length=255)
    slug = models.SlugField('*', unique=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    category_title = models.CharField('Category Title', max_length=255)
    total_votes = models.ManyToManyField(TelegramUser, blank=True)
    
    def __str__(self):
        return self.category_title


class CategoryItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand_name = models.CharField(max_length=255)
    total_votes_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.brand_name

