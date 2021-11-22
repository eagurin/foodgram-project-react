from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name="Название ингредиента", max_length=100, unique=True
    )
    measurement_unit = models.CharField(
        verbose_name="Единица измерения", max_length=20
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return f"{self.name} ({self.measurement_unit})"


class Tag(models.Model):
    BLUE = "#0000FF"
    ORANGE = "#FFA500"
    GREEN = "#008000"
    PURPLE = "#800080"
    YELLOW = "#FFFF00"

    COLOR_CHOICES = [
        (BLUE, "Синий"),
        (ORANGE, "Оранжевый"),
        (GREEN, "Зеленый"),
        (PURPLE, "Фиолетовый"),
        (YELLOW, "Желтый"),
    ]
    name = models.CharField(
        verbose_name="Название тега", max_length=100, unique=True
    )
    color = models.CharField(
        verbose_name="Цвет", max_length=7, unique=True, choices=COLOR_CHOICES
    )
    slug = models.SlugField(
        verbose_name="Слаг",
        max_length=100,
        unique=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name="Автор",
        on_delete=models.CASCADE,
        related_name="recipes",
    )
    name = models.CharField(verbose_name="Название", max_length=100)
    image = models.ImageField(verbose_name="Изображение", upload_to="recipes/")
    text = models.TextField(verbose_name="Описание")
    ingredients = models.ManyToManyField(
        Ingredient,
        through="IngredientAmount",
        verbose_name="Ингредиенты",
        related_name="recipes",
    )
    tags = models.ManyToManyField(Tag, verbose_name="Теги")
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name="Время приготовления (мин.)"
    )
    pub_date = models.DateTimeField(
        "date published", auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ["-pub_date"]
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    ingredients = models.ForeignKey(
        Ingredient,
        verbose_name="Ингредиенты",
        on_delete=models.PROTECT,
        related_name="ingredients_amount",
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name="Рецепт ингредиента",
        on_delete=models.CASCADE,
        related_name="ingredients_amount",
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name="Количество ингредиента",
        validators=[
            MinValueValidator(
                1, 'Количество ингредиентов должно быть больше "0"'
            ),
        ],
    )

    class Meta:
        verbose_name = "Ингредиенты в рецепте"
        verbose_name_plural = "Ингредиенты в рецепте"
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "ingredients"], name="uniq_ingred_amount"
            )
        ]

    def __str__(self):
        return (
            f"Понадобится {self.amount}"
            f"{self.ingredients.measurement_unit}. "
            f'"{self.ingredients.name}"'
            f' для "{self.recipe}"'
        )


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name="Ингридиент",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
    )
    amount = models.PositiveSmallIntegerField(
        validators=(
            MinValueValidator(
                1, message="Минимальное количество ингридиентов 1"
            ),
        ),
        verbose_name="Количество",
    )

    class Meta:
        ordering = ["-id"]
        verbose_name = "Количество ингридиента"
        verbose_name_plural = "Количество ингридиентов"
        constraints = [
            models.UniqueConstraint(
                fields=["ingredient", "recipe"],
                name="unique ingredients recipe",
            )
        ]


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="Рецепт",
    )

    class Meta:
        ordering = ["-id"]
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"],
                name="unique favorite recipe for user",
            )
        ]


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="cart",
        verbose_name="Пользователь",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="cart",
        verbose_name="Рецепт",
    )

    class Meta:
        ordering = ["-id"]
        verbose_name = "Корзина"
        verbose_name_plural = "В корзине"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"], name="unique cart user"
            )
        ]
