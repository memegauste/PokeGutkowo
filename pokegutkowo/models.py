"""PokeGutkowo models file."""
# Django
from django.core.exceptions import ValidationError
from django.db import models

# 3rd-party
from ckeditor.fields import RichTextField

# Create your models here.


class SingleInstanceMixin(object):
    """Makes sure that no more than one instance of a given model is created."""

    def clean(self):  # noqa: D102
        model = self.__class__
        if (model.objects.count() > 0 and self.id != model.objects.get().id):
            raise ValidationError('Można utworzyć tylko 1 {0} instancję!'.format(model.__name__))
        super(SingleInstanceMixin, self).clean()


class Player(models.Model):
    """Player model."""

    INSTINCT = 'instinct'
    MYSTIC = 'mystic'
    VALOR = 'valor'
    POGO_TEAMS = (
        (INSTINCT, 'Instinct'),
        (MYSTIC, 'Mystic'),
        (VALOR, 'Valor'),
    )
    nickname = models.CharField('Nick', max_length=255)
    level = models.IntegerField('Poziom')
    team = models.CharField('Zespół', max_length=255, choices=POGO_TEAMS)
    trainer_code = models.CharField('Kod trenera', max_length=12, null=True, blank=True)

    class Meta:  # noqa: D106
        verbose_name = 'Gracz'
        verbose_name_plural = 'Gracze'

    def __str__(self):  # noqa: D105
        return self.nickname


class Post(models.Model):
    """Post model."""

    title = models.CharField('Tytuł postu', max_length=255)
    context = RichTextField('Treść postu')
    author = models.ForeignKey(Player, on_delete=models.CASCADE)

    class Meta:  # noqa: D106
        verbose_name = 'Post'
        verbose_name_plural = 'Posty'

    def __str__(self):  # noqa: D105
        return self.title


class Settings(SingleInstanceMixin, models.Model):
    """Settings model."""

    title = models.CharField('Nazwa strony', max_length=255, blank=True, null=True)
    owner_acc = models.ForeignKey(Player, on_delete=models.CASCADE, blank=True, null=True)
    owner_about = models.TextField('O właścicielu', blank=True, null=True)
    owner_screenshot = models.ImageField('Screenshot właściciela', blank=True, null=True)
    discord = models.URLField('Link do discorda', max_length=255, blank=True, null=True)

    class Meta:  # noqa: D106
        verbose_name = 'Ustawienia'
        verbose_name_plural = 'Ustawienia'

    def __str__(self):  # noqa: D105
        return 'Ustawienia'
