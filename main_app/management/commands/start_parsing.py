from django.core.management.base import BaseCommand
import subprocess


class Command(BaseCommand):
    help = 'Starts the parsing process'

    def handle(self, *args, **kwargs):
        try:
            command = ['dotnet', r"C:\Users\Asus\PycharmProjects\PriceMatch\main_app\management\commands\Parsers\vkusvill_parser\vkusvil_parser.dll", r'C:\Users\Asus\PycharmProjects\PriceMatch\main_app\management\commands\data\vkusvill_parser_data.json']

            result = subprocess.run(command, capture_output=True, text=True)

            if result.stderr:
                print("C# Errors:")
                print(result.stderr)
        except Exception as e:
            print(f"Ошибка при выполнении: {e}")
