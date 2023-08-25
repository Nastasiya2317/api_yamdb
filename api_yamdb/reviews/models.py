from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator


class User(AbstractUser):
    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"
    ROLES = [
        (USER, _("Authenticated user")),
        (ADMIN, _("Administrator")),
        (MODERATOR, _("Moderator")),
    ]
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _("Username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "Unique": _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_("First name"), max_length=150, blank=True)
    last_name = models.CharField(_("Last name"), max_length=150, blank=True)
    email = models.EmailField(_("Email address"), blank=True)
    role = models.CharField(
        _("Users role"),
        choices=ROLES,
        max_length=30,
        default=USER,
    )
    bio = models.TextField(
        verbose_name="Биография",
        blank=True,
    )

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR


class Genre(models.Model):
    name = models.CharField(_("Genres name"), max_length=100)
    slug = models.SlugField( null=True) 
        
    class Meta:
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class Titles(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    year = models.IntegerField(_("Year"))
    description = models.TextField(_("Description", null=True, blank=True))
    genre = models.ManyToManyField(
        Genre,
        verbose_name=_("Genre"),
        related_name="titles",
        blank=True,
        through="GenreTitles"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="titles",
        verbose_name=_("Category")
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Title")
        verbose_name_plural = _("Titles")
        

class GenreTitles(models.Model):
    titles = models.ForeignKey(Titles, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.genre} {self.titles}"

    class Meta:
        verbose_name = _("Genre and Title")
        verbose_name_plural = _("Genres and Titles")


class Review(models.Model):
    text = models.TextField(verbose_name=_("Text"))
    title = models.ForeignKey(
        Titles,
        verbose_name=_("Title"),
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    author = models.ForeignKey(
        User, verbose_name=_("Author"), on_delete=models.CASCADE, related_name="reviews"
    )
    pub_date = models.DateTimeField(_("Publication date"),
                                    auto_now_add=True, db_index=True
                                    )
    rating = models.IntegerField(_("Feedback score"))

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["title", "author"],
                name="unique_review"
            ),
        ]
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")


class Comment(models.Model): 
    review = models.ForeignKey(
        Review,
        verbose_name=_("Review"),
        on_delete=models.CASCADE,
        related_name="comments",
    )
    text = models.CharField(
        verbose_name=_("Commets text"),
        max_length=256,
    )
    author = models.ForeignKey(
        User,
        verbose_name=_("Author"),
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name=_("Created")
    )

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return self.text
