# import os
# from dotenv import load_dotenv
#
# # Загрузка переменных окружения из .env
# load_dotenv()
#
# class Config:
#     """Базовая конфигурация."""
#     SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key_here')
#     MONGO_URI = os.getenv('MONGO_URI', 'mongodb://mongo:27017/')
    # FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    # FLASK_APP = os.getenv('FLASK_APP', 'run.py')
    # FLASK_RUN_HOST = os.getenv('FLASK_RUN_HOST', '0.0.0.0')

# class DevelopmentConfig(Config):
#     """Конфигурация для разработки."""
#     DEBUG = True
#
# class ProductionConfig(Config):
#     """Конфигурация для production."""
#     DEBUG = False
#
# # Выбор конфигурации в зависимости от FLASK_ENV
# if Config.FLASK_ENV == 'development':
#     config = DevelopmentConfig
# else:
#     config = ProductionConfig