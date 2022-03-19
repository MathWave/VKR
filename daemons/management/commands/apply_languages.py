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
        language_ids = [language.id for language in languages]
        for apply in LanguageApply.objects.all():
            if apply.language_id not in language_ids:
                for s in Set.objects.filter(languages__in=apply.language_id):
                    s.languages.remove(apply.language_id)
                    s.save()
                apply.delete()
