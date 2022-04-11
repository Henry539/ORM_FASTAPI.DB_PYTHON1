import crud
import models
import schemas
import uvicorn
from database import engine, get_db
from fastapi import Depends, FastAPI, HTTPException, Query, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List, Optional

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CONNECT HTML/CSS
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


# LOGIN MAIN PAGE
@app.get("/", response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/form-user", response_class=HTMLResponse)
def create(request: Request):
    return templates.TemplateResponse("create_user.html", {"request": request})


# USER LOGIN SUCCESS
@app.get("/private/{username}", response_class=HTMLResponse)
def user_checked(username: str, request: Request):
    return templates.TemplateResponse("hello.html", {"request": request, "username": username})


@app.get("/user_name/{username}", response_model=schemas.User)
def read_user_by_name(username: str, db: Session = Depends(get_db)):
    data_user = crud.get_user_by_name(db, username)
    if data_user:
        return data_user
    raise HTTPException(status_code=404)


@app.get("/private/{username}/done", response_class=HTMLResponse)
def user_check_done(username: str, request: Request):
    return templates.TemplateResponse("hello-done.html", {"request": request, "username": username})


@app.get("/private/{username}/data", response_class=HTMLResponse)
def read_data_users(username: str, request: Request):
    return templates.TemplateResponse("create_datauser.html", {"request": request, "username": username})


@app.get("/private/{username}/data/update", response_class=HTMLResponse)
def user_update_form(username: str, request: Request):
    return templates.TemplateResponse("update_datauser.html", {"request": request, "username": username})


@app.get("/users", response_model=List[schemas.User])
def read_users(db: Session = Depends(get_db), skip: Optional[int] = 0, limit: Optional[int] = 100):
    db_users = crud.get_all_users(db=db, skip=skip, limit=limit)
    return db_users

@app.get("/users/data", response_model=List[schemas.DataUser])
def read_datausers(db: Session = Depends(get_db), skip: Optional[int]=0, limit: Optional[int]=100):
    db_datausers = crud.get_all_datausers(db=db,skip=skip,limit=limit)
    return db_datausers

@app.post("/check-user")
def check_user(username: str = Form(None), password: str = Form(None), db: Session = Depends(get_db)):
    checkUser = False
    checkPass = False

    data_user = crud.get_user_by_name(db=db, username=username)
    if data_user:
        checkUser = True
        if data_user.PASSWORD == password:
            checkPass = True

    if checkUser and checkPass:
        if data_user.DATA_USER != []:
            return RedirectResponse(url=f"/private/{username}/done", status_code=302)
        return RedirectResponse(url=f"/private/{username}", status_code=302)
    return RedirectResponse(url="/try-back")


@app.post("/try-back", response_class=HTMLResponse)
def login_again(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/create-user", response_model=schemas.UserCreate)
def create_user(username: str = Form(None), password: str = Form(None), db: Session = Depends(get_db)):
    if username != None and password != None:
        data_user = crud.get_user_by_name(db=db, username=username)
        if data_user: raise HTTPException(status_code=400, detail="Email already registered")
        crud.create_user(db=db, username=username, password=password)
        return RedirectResponse(url="/", status_code=302)
    return RedirectResponse(url="/form-user", status_code=302)

@app.post("/create-datauser/{username}")
def create_dateUser(*, username: str, full_name: str = Form(...),
                    age: int = Form(...), sex: str = Form(...), phone: int = Form(...), db: Session = Depends(get_db)):
    data_return = crud.get_user_by_name(db=db, username=username)
    phone=str(phone).zfill(10)
    crud.create_datauser(db=db, full_name=full_name, age=age, sex=sex, phone=phone, user_id=data_return.ID)
    return RedirectResponse(url=f"/private/{username}/done", status_code=302)


@app.post("/update-datauser/{username}")
def create_dateUser(*, username: str, full_name: str = Form(None),
                    age: int = Form(None), sex: str = Form(None), phone: int = Form(None),
                    db: Session = Depends(get_db)):
    data_return = crud.get_user_by_name(db=db, username=username)
    data_user_return = crud.get_datauser(db=db, user_id=data_return.ID)
    update = data_user_return[-1]
    if full_name == None:
        full_name = update.FULLNAME
    if sex == None:
        sex = update.SEX
    if age == None:
        age = update.AGE
    if phone == None:
        phone = update.PHONE
    phone=str(phone).zfill(10)
    crud.create_datauser(db=db, full_name=full_name, age=age, sex=sex, phone=phone, user_id=data_return.ID)

    return RedirectResponse(url=f"/private/{username}/done", status_code=302)




if __name__ == "__main__":
    uvicorn.run("main:app", host="192.168.2.235", port=8002, reload=True)
