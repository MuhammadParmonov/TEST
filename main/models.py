from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# from datetime import datetime

class Category(models.Model):
    name = models.CharField(max_length=60, verbose_name="nomi")
    
    def __str__(self):
        return str(self.name)
    
    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"

class Test(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="avtor")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="kategoriya")
    title = models.CharField(max_length=250, verbose_name="sarlavha")
    max_attemps = models.PositiveIntegerField(verbose_name="maksimum harakatlar soni")
    start_date = models.DateTimeField(default=timezone.now, verbose_name="boshlanish sanasi")
    end_date = models.DateTimeField(default=(timezone.now()+timezone.timedelta(days=2)), verbose_name="tugatish sanasi")
    
    def __str__(self):
        return str(self.title)
    
    class Meta:
        verbose_name = "Test"
        verbose_name_plural = "Testlar"

class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name="test")
    question = models.CharField(max_length=400, verbose_name="savol")
    answer_a = models.CharField(max_length=250, verbose_name="a javob")
    answer_b = models.CharField(max_length=250, verbose_name="b javob")
    answer_c = models.CharField(max_length=250, verbose_name="c javob")
    answer_d = models.CharField(max_length=250, verbose_name="d javob")
    true_answer = models.CharField(max_length=250, verbose_name="to'g'ri javob javob")
    
    def __str__(self):
        return str(f"Question of{self.test.title}: {self.question}")
    
    class Meta:
        verbose_name = "Savol"
        verbose_name_plural = "Savollar"