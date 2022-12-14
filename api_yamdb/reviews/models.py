from django.db import models


class Genre(models.Model):
    name = models.CharField('Жанр', max_length=100)
    slug = models.SlugField(unique=True, max_length=40)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name[:15]


class Category(models.Model):
    name = models.CharField('Категория', max_length=100)
    slug = models.SlugField(unique=True, max_length=40)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name[:30]


class Title(models.Model):
    name = models.CharField('Произведение', max_length=100)
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        related_name='categories',
        null=True,
        blank=True,
    )
    genre = models.ManyToManyField(Genre, through='GenreTitle')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['name']

    def __str__(self):
        return self.name[:30]


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
    )
    genre = models.ForeignKey(
        Genre,
        verbose_name='Жанр',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Произведение и жанр'
        verbose_name_plural = 'Произведения и жанры'

    def __str__(self):
        return (
            f'Произведение:{self.title[:30]},'
            f'\nЖанр:{self.genre[:30]}'
        )
