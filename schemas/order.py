from pydantic import BaseModel


class SubscriptionSchema(BaseModel):
    hello_asso_id: int
    first_name: str
    last_name: str
    email: str
    campagne: str
    type: str
    amount: int
    date: str
    twitter: str
    facebook: str
    instagram: str
    url: str
    name: str
