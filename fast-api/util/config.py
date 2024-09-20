from app._version import __version__
from pydantic import field_validator, SecretStr
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource
from secret_manager import SecretManagerConfigSettingsSource
from typing import Tuple, Type, List

class DatadogServiceConfig(BaseSettings):
    DD_AGENT_STATSD_HOST: str = "127.0.0.1"
    DD_AGENT_STATSD_PORT: int = 8125
    DD_ENV: str = "test"
    DD_LOGS_INJECTION: bool = False
    DD_METRIC_PREFIX: str = "fast.api.microservice.boilerplate"
    DD_PRIORITY_SAMPLING: bool = True
    DD_PROFILING_ENABLED: bool = False
    DD_RUNTIME_METRICS_ENABLED: bool = False
    DD_SAMPLE_RATE: float = 0.1
    DD_SERVICE: str = "fast-api-microservice-boilerplate"
    DD_TRACE_AGENT_URL: str = "unix:///var/run/datadog/apm.socket"
    DD_TRACE_ENABLED: bool = False
    DD_TRACE_HEADER_TAGS: str = ""
    DD_TRACE_SETTING_FILTERS: List[str] = [r"^https?://.*/alive$"]
    DD_SERVICE_TYPE: str = "API"
    DD_VERSION: str = __version__

    @field_validator("DD_ENV")
    def lowercase_datadog_environment(cls, v):
        return v.lower() if isinstance(v, str) else v
    

class SecretsConfig(BaseSettings):
    DB_IP: SecretStr
    DB_PASSWORD: SecretStr

    @classmethod
    def settings_customise_sources(
            cls,
            settings_cls: Type[BaseSettings],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            SecretManagerConfigSettingsSource(settings_cls),
            env_settings,
            file_secret_settings,
        )


class Config(BaseSettings):
    APPLICATION_NAME: str = "Fast API Microservice Boilerplate" #TODO: Replace placeholder
    ENVIRONMENT: str = "test"
    DB_USER: str = "postgres"

    datadog: DatadogServiceConfig = DatadogServiceConfig()
    secrets: SecretsConfig = SecretsConfig()

    @field_validator("ENVIRONMENT")
    def lowercase_environment(cls, v):
        return v.lower() if isinstance(v, str) else v


config: Config = Config()
