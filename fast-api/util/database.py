import string

from config import config


def build_postgres_url() -> str:
    """
    Build a postgres access URL from environment

    :returns: postgres string
    """
    database_ip = config.secrets.DB_IP.get_secret_value()
    database_port = "5432"
    database_user = config.DB_USER
    database_password = config.secrets.DB_PASSWORD.get_secret_value()
    database_name = "db" #TODO: Replace placeholder

    postgres_url_template = string.Template(
        'postgresql://${user}:${password}@${ip}:${port}/{db_name}?application_name=${app}')
    postgres_url = postgres_url_template.substitute(
        user=database_user,
        password=database_password,
        ip=database_ip,
        port=database_port,
        db_name=database_name,
        app='fast-api-microservice-boilerplate'
    )
    return postgres_url
