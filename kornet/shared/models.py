import yaml
from pydantic import BaseModel, SecretStr


class Model(BaseModel):
    def yaml(self) -> str:
        return yaml.dump(self.dict())


class SSHProps(Model):
    port: int = 22
    username: str = "root"
    password: SecretStr = SecretStr("root")
