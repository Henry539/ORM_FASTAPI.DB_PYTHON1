from typing import List, Optional

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Query, Request, Form
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import crud, models, schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


#CONNECT HTML/CSS
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


#LOGIN MAIN PAGE
@app.get("/", response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


#CREATE NEW USER FORM
@app.get("/form-user", response_class=HTMLResponse)
def create(request: Request):
    return templates.TemplateResponse("create_user.html", {"request": request})

#USER LOGIN SUCCESS
@app.get("/private", response_class=HTMLResponse)
def user_checked(username: str, request: Request):
    return templates.TemplateResponse("hello.html", {"request": request,"username": username.upper()})


@app.get("/user_name/{username}", response_model=schemas.User)
def read_user_by_name(username: str, db: Session = Depends(get_db)):
    data_user = crud.get_user_by_name(db, username)
    if data_user: return data_user
    raise HTTPException(status_code=404)


@app.get("/user_id/{user_id}", response_model=schemas.User)
def read_user_by_id(user_id: int, db: Session = Depends(get_db)):
    data_user = crud.get_user(db, user_id)
    if data_user: return data_user
    raise HTTPException(status_code=404)


@app.get("/users", response_model=List[schemas.User])
def read_users(db: Session = Depends(get_db), skip: Optional[int] = 0, limit: Optional[int] = 100):
    db_users = crud.get_all_users(db=db, skip=skip, limit=limit)
    return db_users

@app.post("/check-user")
def check_user(username: str = Form(None), password: str = Form(None),db: Session = Depends(get_db)):
    checkUser = False
    checkPass = False

    data_user = crud.get_user_by_name(db= db, username=username)
    if data_user:
        checkUser = True
        if data_user.PASSWORD == password:
            checkPass = True

    if checkUser and checkPass:
        return RedirectResponse(url=f"/private?username={username}", status_code=302)
    return RedirectResponse(url="/try-back")

#USER LOGIN REBACK
@app.post("/try-back", response_class=HTMLResponse)
def login_again(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})




@app.post("/create-user", response_model=schemas.UserCreate)
def create_user(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    data_user = crud.get_user_by_name(db=db, username=username)
    if data_user: raise HTTPException(status_code=400, detail="Email already registered")
    crud.create_user(db=db, username=username, password=password)
    return RedirectResponse(url="/", status_code=302)


@app.post("/user/data", response_model=schemas.DataUser)
def create_dateUser(*, user_id: int = Query(None, description="Choose 1 in UserID or UserName"),
                    user_name: str = Query(None, description="Choose 1 in UserID or UserName"), full_name: str,
                    age: int, sex: str, phone: int, db: Session = Depends(get_db)):
    if user_name != None and user_id == None:
        data_return = crud.get_user_by_name(db=db, username=user_name)
        if data_return: return crud.create_datauser(db=db, full_name=full_name, age=age, sex=sex, phone=phone,
                                                    user_id=data_return.ID)
        raise HTTPException(status_code=403)
    elif user_id != None and user_name == None:
        data_return = crud.get_user(db=db, user_id=user_id)
        if data_return: return crud.create_datauser(db=db, full_name=full_name, age=age, sex=sex, phone=phone,
                                                    user_id=user_id)
        raise HTTPException(status_code=403)
    raise HTTPException(status_code=404)



if __name__ == "__main__":
    uvicorn.run("main:app", port=8002)
