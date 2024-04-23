# import_django_users.py
import csv
import django
import os

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proypostgrado.settings")
django.setup()

from django.contrib.auth.models import User

def import_users_from_csv(csv_file_path):
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Asumimos que tu CSV tiene 'username', 'password', 'email', 'first_name', 'last_name'
            username = row['username']
            password = row['password']
            email = row['email']
            first_name = row['first_name']
            last_name = row['last_name']

            # Verificar si el usuario ya existe
            if not User.objects.filter(username=username).exists():
                user = User(username=username, email=email, first_name=first_name, last_name=last_name)
                user.set_password(password)
                user.save()
                print(f'Usuario {username} creado exitosamente.')
            else:
                print(f'El usuario {username} ya existe.')

if __name__ == "__main__":
    csv_file_path = 'C:/Users/mijha/Desktop/Nueva carpeta/usuarios.csv'  # Asegúrate de cambiar esto por la ruta real a tu archivo CSV
    import_users_from_csv(csv_file_path)
