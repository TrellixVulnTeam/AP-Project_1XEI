class Config:
    DEBUg = True

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:admin@localhost/reservation_system'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'super-secret-key'
    JWT_ERROR_MESSAGE_KEY = 'message'
