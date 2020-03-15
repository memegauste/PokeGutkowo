from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.


class SingleInstanceMixin(object):
    '''Makes sure that no more than one instance of a given model is created.'''

    def clean(self):
        model = self.__class__
        if (model.objects.count() > 0 and self.id != model.objects.get().id):
            raise ValidationError('Można utworzyć tylko 1 {0} instancję!'.format(model.__name__))
        super(SingleInstanceMixin, self).clean()


POGO_TEAMS = (
        ('instinct', 'Instinct'),
        ('mystic', 'Mystic'),
        ('valor', 'Valor'),
)


class Players(models.Model):
    nickname = models.CharField('Nick', max_length=255)
    level = models.IntegerField('Poziom')

    team = models.CharField('Zespół', max_length=255, choices=POGO_TEAMS)
    trainer_code = models.CharField('Kod trenera', max_length=12, null=True, blank=True)

    class Meta:
        verbose_name = 'Gracz'
        verbose_name_plural = 'Gracze'

    def __str__(self):
        return self.nickname


class Post(models.Model):
    title = models.CharField('Tytuł postu', max_length=255)
    context = RichTextField('Treść postu')
    author = models.ForeignKey(Players, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posty'

    def __str__(self):
        return self.title


class Settings(SingleInstanceMixin, models.Model):
    title = models.CharField('Nazwa strony', max_length=255)
    owner_acc = models.ForeignKey(Players, on_delete=models.CASCADE)
    owner_about = models.TextField('O właścicielu')
    owner_screenshot = models.ImageField('Screenshot właściciela')
    discord = models.URLField('Link do discorda', max_length=255)

    class Meta:
        verbose_name = 'Ustawienia'
        verbose_name_plural = 'Ustawienia'

    def __str__(self):
        return 'Ustawienia'
