import logging
from google.auth import default as gc_auth_default
from google.cloud.secretmanager_v1 import SecretManagerServiceClient
from google.api_core.exceptions import NotFound, PermissionDenied
from google.auth.exceptions import DefaultCredentialsError
from os import environ
from pydantic.fields import FieldInfo
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource
from typing import Any, Dict, Optional, Tuple, Type


logger = logging.getLogger(__name__)


class SecretManagerConfigSettingsSource(PydanticBaseSettingsSource):
    """
        A settings class that loads settings from Google Secret Manager.

        The account under which the application is executed should have the
        required access to Google Secret Manager.
    """

    def __init__(self, settings_cls: Type[BaseSettings]):
        super().__init__(settings_cls)
        logger.debug('Initializing Google Secrets Manager Config Settings Source')
        self._client = None
        self._project_id = None

    def __get_secret_by_name(self, field_name: str) -> Optional[str]:
        logger.debug(f'Getting secret for {field_name}')
        return self._client.access_secret_version(
            name=environ[field_name]).payload.data.decode().strip()

    def get_field_value(
        self, field: FieldInfo, field_name: str
    ) -> Tuple[Any, str, bool]:
        """
        Get the value of a field from Google Secret Manager.
        """
        try:
            field_name = field.alias or field_name
            field_value = self.__get_secret_by_name(field_name)
        except (NotFound, PermissionDenied) as e:
            logger.debug(e)
            field_value = None

        return field_value, field_name, False

    def __call__(self) -> Dict[str, Any]:
        secrets: Dict[str, Any] = {}

        try:
            # Set the credentials and project ID from the application default credentials
            _credentials, project_id = gc_auth_default()
            self._project_id = project_id
            self._client = SecretManagerServiceClient(
                credentials=_credentials
            )

            for field_name, field in self.settings_cls.model_fields.items():
                field_value, field_key, value_is_complex = self.get_field_value(
                    field, field_name
                )
                field_value = self.prepare_field_value(
                    field_name, field, field_value, value_is_complex
                )
                if field_value is not None:
                    secrets[field_key] = field_value

        except DefaultCredentialsError as e:
            logger.debug(str(e))

        return secrets
