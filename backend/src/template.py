from pydantic import BaseModel, validator


class Insurer(BaseModel):
    name: str = "None"
    siren: str = "None"

    @validator('*')
    def type_check(cls, v):
        if not isinstance(v, str):
            raise TypeError('must be string')


class Product(BaseModel):
    typology: str = "None"
    product: str = "None"
    description: str = "None"

    @validator('*')
    def type_check(cls, v):
        if not isinstance(v, str):
            raise TypeError('must be string')


class Coverage(BaseModel):
    always_covered: str = "None"
    optionally_covered: str = "None"
    not_covered: str = "None"
    exclusions: str = "None"
    services: str = "None"

    @validator('*')
    def type_check(cls, v):
        if not isinstance(v, str):
            raise TypeError('must be string')


class Applicability(BaseModel):
    obligations: str = "None"
    localization: str = "None"
    payment_options: str = "None"
    start_date: str = "None"
    termination: str = "None"

    @validator('*')
    def type_check(cls, v):
        if not isinstance(v, str):
            raise TypeError('must be string')


class Ipid(BaseModel):
    insurer: Insurer = Insurer()
    product: Product = Product()
    coverage: Coverage = Coverage()
    applicability: Applicability = Applicability()
