from ninja import Schema
from pydantic import validator
from ninja.errors import HttpError


class LoginSchemas(Schema):
    username: str
    motPasse: str


class Initialisation(Schema):
    amount: int
    description: str
    customer_name: str
    customer_surname: str
    customer_phone_number: str

    @validator('amount')
    def validate_amount(cls, value):
        if value % 5 != 0 or value < 100:
            raise HttpError(
                status_code=400, message='Amount must be a multiple of 5 and greater than or equal to 100')
        return value


class EcolbetIdSchemas(Schema):
    ecolbet_id: str


class TokenSchemas(Schema):
    token: str


class MySoleaPay(Schema):
    operator : int
    customer_number : str
    amount:float