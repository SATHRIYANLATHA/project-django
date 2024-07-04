from blog.models import Category
from typing import Any
from django.core.management.base import BaseCommand




class Command(BaseCommand):
    help="THIS COMMANDS INSERTS CATEGORY DATA"


    def handle(self,*args:Any, **options:Any):

        # DELETE EXISTING DATA
        Category.objects.all().delete()

        categories=['Sports','Technology','Science','Art','Food']
        
        for category_name in categories:
            Category.objects.create(name = category_name)


        
        self.stdout.write(self.style.SUCCESS("COMPLETED INSERTING DATA"))