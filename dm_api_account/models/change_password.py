from pydantic import BaseModel, Field, ConfigDict

class ChangePassword(BaseModel):
    model_config = ConfigDict(extra="forbid")
    login: str = Field(..., description="Логин")
    old_password: str = Field(..., description="Старый пароль", serialization_alias="oldPassword")
    new_password: str = Field(..., description="Новый пароль", serialization_alias="newPassword")
    token: str = Field(..., description="Токен для смены пароля")