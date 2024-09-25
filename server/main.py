import uuid
import sqlmodel as sql
from fastapi import FastAPI, Response, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from .database import get_session
from .models import Admin, AdminCreate, HealthcareAdvisor, Stock, LoginSchema
from .utils import sessions, login_admin, get_session_id, get_current_admin, hash_password, verify_password


# instance
app = FastAPI()

origins = [
    "http://localhost:3000", # fontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# root route
@app.get("/")
def root():
    return {"message": "hello world"}

# create admin
@app.post("/api/auth/register")
def register_Admin(*, session: sql.Session = Depends(get_session), admin: AdminCreate):
    already_exists = session.exec(sql.select(Admin).where(Admin.email == admin.email)).first()
    if already_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Admin with this email is already registered."
        )

    admin.first_name = admin.first_name.lower()
    admin.last_name = admin.last_name.lower()
    admin.province = admin.province.lower()
    admin.district = admin.district.lower()
    admin.sector = admin.sector.lower()
    admin.cell = admin.cell.lower()
    admin.email = admin.email.lower()

    admin.password_hashed = hash_password(admin.password_hashed)

    db_admin = Admin.model_validate(admin)
    session.add(db_admin)
    session.commit()
    session.refresh(db_admin)

    statement = sql.select(HealthcareAdvisor).where(
        (HealthcareAdvisor.province == db_admin.province) &
        (HealthcareAdvisor.district == db_admin.district) &
        (HealthcareAdvisor.sector == db_admin.sector) &
        (HealthcareAdvisor.cell == db_admin.cell)
    )
    healthcare_advisors = session.exec(statement).all()
    for advisor in healthcare_advisors:
        advisor.admin_id = db_admin.id 
        session.add(advisor)
    session.commit()
    return {
        "message": "Ok",
        "data": db_admin
    }



# admin login
@app.post("/api/auth/login")
def login(*, session: sql.Session = Depends(get_session), login_data: LoginSchema, response: Response):
    email = login_data.email
    password = login_data.password

    admin = session.exec(sql.select(Admin).where(Admin.email == email)).first()
    if not admin or not verify_password(password, admin.password_hashed):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    session_id = str(uuid.uuid4())
    login_admin(session_id, admin.id)
    response.set_cookie(key="session_id", value=session_id, httponly=True, samesite="Lax")
    return {"message": "Login successful", "admin_id": admin.id, "session_id": session_id}


# filter healthcare advisors and stock levels based on admin's region
@app.get("/api/dashboard")
def get_admin_dashboard(
    *,
    session_id: str = Depends(get_session_id),  
    session: sql.Session = Depends(get_session),
    admin: Admin = Depends(get_current_admin)
):
    if session_id is None or session_id not in sessions:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    # print("dash-session_id: ", session_id)
    statement = sql.select(HealthcareAdvisor).where(HealthcareAdvisor.admin_id == admin.id)
    advisors = session.exec(statement).all()

    stock_levels = []
    for advisor in advisors:
        statement = sql.select(Stock).where(Stock.healthcare_advisor_id == advisor.id)
        stocks = session.exec(statement).all()
        stock_levels.extend(stocks)

    if not advisors:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No healthcare advisors found.")
    if not stock_levels:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No stock levels found.")

    return {
        "admin": admin,
        "advisors": advisors,
        "stock_levels": stock_levels
    }
 

