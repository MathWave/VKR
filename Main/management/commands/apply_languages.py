from django.core.management.base import BaseCommand

from Main.models import LanguageApply, Set
from SprintLib.language import languages


class Command(BaseCommand):
    help = "starts FileStorage"

    def handle(self, *args, **options):
        for language in languages:
            apply = LanguageApply.objects.filter(language_id=language.id, applied=True).first()
            if apply is None:
                for s in Set.objects.filter(auto_add_new_languages=True):
                    if language.id not in s.languages:
                        s.languages.append(language.id)
                        s.save()
                obj, _ = LanguageApply.objects.get_or_create(language_id=language.id)
                obj.applied = True
                obj.save()
