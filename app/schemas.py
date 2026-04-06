from pydantic import BaseModel


class CarBase(BaseModel):
    id: int
    model: str
    number: str
    is_reserved: bool

    class Config:
        from_attributes = True


class CarInfo(BaseModel):
    id: int
    car_model: str
    car_number: str
    fuel_level: str

    class Config:
        from_attributes = True


class CarInfoAuthRequest(BaseModel):
    phone: str
    sms_code: str

