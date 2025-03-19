import json
import os
from django.core.management.base import BaseCommand
from main_app.models import Product, Shop

class Command(BaseCommand):
    help = "Loads data from products.json and updates the database"

    def add_arguments(self, parser):
        parser.add_argument('json_file_path', type=str, help='The path to the JSON file to be processed')

    def handle(self, *args, **options):
        json_file_path = options['json_file_path']

        if not os.path.exists(json_file_path):
            self.stdout.write(self.style.ERROR("Файл products.json не найден"))
            return
        shop = Shop.objects.get(id=3)


        try:
            with open(json_file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, list):
                self.stdout.write(self.style.ERROR("Неверный формат JSON. Ожидается список товаров."))
                return


            for item in data:
                product = Product.objects.create(
                    name=item["name"],
                    price=item.get("price", 0),
                    image=item["image"],
                    shop=shop
                )

                self.stdout.write(self.style.SUCCESS(f"Обновлен товар: {product.name}"))

            self.stdout.write(self.style.SUCCESS("Данные успешно загружены в базу"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ошибка при загрузке JSON: {e}"))
