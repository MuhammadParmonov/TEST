from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from .models import CheckTest, ChekQuestion

# pre_save()
# save()
# post_save()

@receiver(pre_save, sender=CheckTest)
def calculate_test(sender, instance, *args, **kwargs):
    questions = ChekQuestion.objects.filter(checktest=instance)
    
    number_of_question = questions.count()
    number_of_true_answers = questions.filter(is_true=True).count()
    try: 
        percentage = number_of_true_answers / number_of_question * 100
    except:
        percentage = 0
        
    instance.true_answers = number_of_true_answers
    instance.percentage = percentage
    if instance.test.pass_percentage < percentage:
        instance.is_passed = True

@receiver(pre_save, sender=ChekQuestion)
def checkquestion(sender, instance, *args, **kwargs):
    if instance.given_answer == instance.true_answer:
        instance.is_true = True
    else:
        instance.is_true = False