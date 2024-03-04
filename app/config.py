import os
from typing import Union
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "prov-tools API"
    admin_email: str

    netbox_secret: str

    '''
    Note that if deployed via a container, especially with EKS, a config map will be used
    such that required variables are implemented as environment variables.
    
    db_region: str = os.getenv('DB_REGION', default='us-east-1')
    db_access_key_id: Union[str, None] = os.getenv('DB_ACCESS_KEY_ID')
    db_secret_access_key: Union[str, None] = os.getenv('DB_SECRET_ACCESS_KEY')
    db_endpoint_url: Union[str, None] = os.getenv('DB_ENDPOINT_URL')
    '''

    db_region: str
    db_access_key_id: str
    db_secret_access_key: str
    db_endpoint_url: str

    model_config = SettingsConfigDict(env_file=".env")
