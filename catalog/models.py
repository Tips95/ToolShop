from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название категории")
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class Tool(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    stock = models.IntegerField(verbose_name="Количество на складе")
    image = models.ImageField(upload_to='tools/', null=True, blank=True, verbose_name="Изображение")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name="Категория")
    is_popular = models.BooleanField(default=False, verbose_name="Популярный товар")  # Новое поле

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Инструмент"
        verbose_name_plural = "Инструменты"