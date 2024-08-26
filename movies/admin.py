from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *
from .forms import MovieAdminForm


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'url']
    list_display_links = ['name', 'description', 'url']


class CommentInline(admin.TabularInline):
    model = Comments
    extra = 0
    readonly_fields = ['name', 'email']


class MovieShotsInline(admin.TabularInline):
    model = MovieShots
    extra = 1
    readonly_fields = ['get_image']

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="80px" height="60px">')

    get_image.short_description = "Кадр из фильма"


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'url', 'draft']
    list_display_links = ['title', 'category', 'url']
    list_filter = ['category', 'year']
    list_editable = ['draft']
    search_fields = ['title', 'category__name']
    actions = ['publish', 'unpublish']
    form = MovieAdminForm
    inlines = [MovieShotsInline, CommentInline]
    save_on_top = True
    save_as = True
    readonly_fields = ['get_image']
    fieldsets = (
        ("Common Data", {
            "fields": (("title", "tagline", "description", "poster", "get_image"),)
        }),
        ("Release", {
            "fields": (("year", "premiere_date", "country"),)
        }),
        ("Members", {
            "classes": ("collapse",),
            "fields": (("actors", "directors"),)
        }),
        ("Type", {
            "fields": (("category", "genres"),)
        }),
        ("Budget", {
            "fields": (("budget", "fees_in_usa", "fees_in_world"),)
        }),
        ("Option", {
            "fields": (("url", "draft"),)
        }),
    )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="100px" height="auto">')

    def unpublish(self, request, queryset):
        """Снять с публикации"""
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")

    def publish(self, request, queryset):
        """Опубликовать"""
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")

    publish.short_description = 'Опубликовать'
    publish.allowed_permissions = ('change', )

    unpublish.short_description = 'Снять с публикации'
    unpublish.allowed_permissions = ('change', )

    get_image.short_description = "Постер"


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'receiver', 'movie']
    list_display_links = ['name', 'email', 'receiver', 'movie']
    readonly_fields = ['name', 'email']
    search_fields = ['name', 'email', 'receiver', 'movie__title']


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ['name', 'birthday', 'get_image']
    list_display_links = ['name', 'birthday']
    readonly_fields = ['get_image']

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60">')

    get_image.short_description = "Изображение"


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'url']
    list_display_links = ['name', 'description', 'url']


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    list_display = ['title', 'movie', 'get_image']
    list_display_links = ['title', 'movie']
    readonly_fields = ['get_image']

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="80" height="60">')

    get_image.short_description = "Изображение"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['ip', 'star', 'movie']
    list_display_links = ['ip', 'star', 'movie']


admin.site.register(RatingStar)

