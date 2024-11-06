from pydantic import BaseModel, Field, ConfigDict

class ChangePassword(BaseModel):
    model_config = ConfigDict(extra="forbid")
    login: str = Field(..., description="Логин")
    old_password: str = Field(..., description="Старый пароль")
    new_password: str = Field(..., description="Новый пароль")
    token: str = Field(..., description="Токен для смены пароля")