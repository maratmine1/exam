from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from . import models, schemas
from .database import Base, engine, get_db

app = FastAPI(title="Carsharing API")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def init_db() -> None:
    Base.metadata.create_all(bind=engine)

    db = next(get_db())
    try:
        if not db.query(models.Car).first():
            cars = [
                models.Car(id=1, model="Kia Rio", number="o787oo50", is_reserved=True),
                models.Car(id=2, model="VW Polo", number="e887eo777", is_reserved=False),
                models.Car(id=3, model="VW Polo", number="m761oh797", is_reserved=True),
                models.Car(id=4, model="Toyota RAV4", number="H761oH797", is_reserved=True),
            ]
            db.add_all(cars)

        if not db.query(models.Trip).first():
            trips = [
                models.Trip(
                    id=1,
                    phone="+79846274627",
                    sms_code="1420",
                    car_model="Kia Rio",
                    car_number="o787oo50",
                    fuel_level="76%",
                ),
                models.Trip(
                    id=2,
                    phone="+79175628572",
                    sms_code="1100",
                    car_model="VW Polo",
                    car_number="m761oh797",
                    fuel_level="56%",
                ),
                models.Trip(
                    id=3,
                    phone="+7916552451",
                    sms_code="1100",
                    car_model="Toyota RAV4",
                    car_number="H761oH797",
                    fuel_level="11%",
                ),
            ]
            db.add_all(trips)

        db.commit()
    finally:
        db.close()


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/cars", response_model=list[schemas.CarBase], summary="Получение информации о свободных машинах")
def get_available_cars(db: Session = Depends(get_db)):
    cars = db.query(models.Car).filter(models.Car.is_reserved.is_(False)).all()
    return cars


@app.post(
    "/car-info",
    response_model=schemas.CarInfo,
    summary="Получение информации о выбранном автомобиле (с аутентификацией)",
)
def get_car_info(auth: schemas.CarInfoAuthRequest, db: Session = Depends(get_db)):
    trip = (
        db.query(models.Trip)
        .filter(models.Trip.phone == auth.phone, models.Trip.sms_code == auth.sms_code)
        .first()
    )

    if trip is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверная пара телефон + СМС код",
        )

    return trip

