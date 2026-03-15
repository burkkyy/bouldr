from src.app import create_app
from src.services.seeder import seed_data


app = create_app()

with app.app_context():
    result = seed_data()
    print(result)