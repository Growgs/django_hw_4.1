from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Scope, Topic


class RelationshipInlineFormset(BaseInlineFormSet):
    def clean(self):
        counter = 0
        for form in self.forms:
            if form.cleaned_data.get('is_main'):
                counter += 1
            else:
                continue
        if counter > 1:
            raise ValidationError('Основным может быть только один раздел')
        elif counter == 0:
            raise ValidationError('Укажите основной раздел')
        return super().clean()


class ScopingInline(admin.TabularInline):
    model = Scope
    formset = RelationshipInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopingInline]


@admin.register(Topic)
class ScopesAdmin(admin.ModelAdmin):
    pass
