from typing import List

from pydantic import BaseModel, validator


class Insurer(BaseModel):
    name: str = ""
    siren: List = []

    @validator('name')
    def type_check_name(cls, v):
        if not isinstance(v, str):
            raise TypeError('must be string')

    @validator('siren')
    def type_check_siren(cls, v):
        if not isinstance(v, List):
            raise TypeError('must be list')


class Product(BaseModel):
    typology: str = ""
    product: str = ""
    description: str = ""

    @validator('*')
    def type_check(cls, v):
        if not isinstance(v, str):
            raise TypeError('must be string')


class Coverage(BaseModel):
    always_covered: str = ""
    optionally_covered: str = ""
    not_covered: str = ""
    exclusions: str = ""
    services: str = ""

    @validator('*')
    def type_check(cls, v):
        if not isinstance(v, str):
            raise TypeError('must be string')


class Applicability(BaseModel):
    obligations: str = ""
    localization: str = ""
    payment_options: str = ""
    start_date: str = ""
    termination: str = ""

    @validator('*')
    def type_check(cls, v):
        if not isinstance(v, str):
            raise TypeError('must be string')


class Ipid(BaseModel):
    insurer: Insurer = Insurer()
    product: Product = Product()
    coverage: Coverage = Coverage()
    applicability: Applicability = Applicability()
