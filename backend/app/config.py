"""Application settings, loaded from environment variables."""

from decimal import Decimal

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.constants import PERCENT_BASE
from app.domain.tolerance import DEFAULT_TOLERANCE_POLICY, TolerancePolicy


class ToleranceTierSetting(BaseModel):
    min_budget: Decimal
    tolerance_percent: Decimal


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg://evm:evm@localhost:5432/evm"
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]
    # JSON list in the TOLERANCE_TIERS environment variable. When unset, the defaults apply.
    tolerance_tiers: list[ToleranceTierSetting] | None = None

    @property
    def tolerance_policy(self) -> TolerancePolicy:
        if self.tolerance_tiers is None:
            return DEFAULT_TOLERANCE_POLICY
        return TolerancePolicy.from_pairs(
            (tier.min_budget, tier.tolerance_percent / PERCENT_BASE)
            for tier in self.tolerance_tiers
        )


settings = Settings()
