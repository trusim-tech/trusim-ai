from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    google_api_key: str = ""
    gemini_model: str = "gemini-3-flash-preview"
    backend_url: str = "http://localhost:8080"
    backend_ws_url: str = "ws://localhost:8081"
    backend_grpc_url: str = "http://localhost:8082"
    nokia_api_key: str = ""
    fastapi_port: int = 8090
    ws_port: int = 8091

    class Config:
        env_file = ".env"


settings = Settings()
