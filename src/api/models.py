"""Pydantic response contracts for the Insurance Risk Intelligence API."""
from pydantic import BaseModel

class HealthResponse(BaseModel):
    status: str
    application: str

class DatabaseHealthResponse(BaseModel):
    status: str
    database: str
    connection: str

class DashboardSummaryResponse(BaseModel):
    total_policies: int
    total_observations: int
    total_premium: float
    total_claims_cost: float
    average_premium: float
    total_exposure: float

class YearlyMetric(BaseModel):
    period: int
    total_observations: int
    total_policies: int
    total_premium: float
    total_claims_cost: float
    average_premium: float
    total_exposure: float

class YearlyResponse(BaseModel):
    years: list[YearlyMetric]

class ProductMetric(BaseModel):
    type_product: str | None
    reimbursement: str | None
    total_observations: int
    total_policies: int
    total_premium: float
    total_claims_cost: float
    average_premium: float
    total_exposure: float

class ProductsResponse(BaseModel):
    products: list[ProductMetric]

class ChannelMetric(BaseModel):
    distribution_channel: str | None
    total_observations: int
    total_policies: int
    total_premium: float
    total_claims_cost: float
    average_premium: float
    total_exposure: float

class ChannelsResponse(BaseModel):
    channels: list[ChannelMetric]

class PolicyMetric(BaseModel):
    type_policy: str | None
    type_policy_dg: str | None
    total_observations: int
    total_policies: int
    total_premium: float
    total_claims_cost: float
    average_premium: float
    total_exposure: float

class PoliciesResponse(BaseModel):
    policies: list[PolicyMetric]

class CustomerMetric(BaseModel):
    gender: str | None
    total_observations: int
    total_customer_records: int
    total_policies: int
    total_premium: float
    total_claims_cost: float
    average_premium: float
    total_exposure: float

class CustomersResponse(BaseModel):
    customers: list[CustomerMetric]

class CustomerCohortMetric(BaseModel):
    year_effect_insured: int | None
    total_observations: int
    total_customer_records: int
    total_policies: int
    total_premium: float
    total_claims_cost: float
    average_premium: float
    total_exposure: float

class CustomerCohortsResponse(BaseModel):
    customer_cohorts: list[CustomerCohortMetric]
