import os
import jwt

from fastapi import FastAPI, Depends, HTTPException, Cookie, Response, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select, Date, func
from sqlalchemy.orm import Session

from models import User, Wishlist, Product, Cart, Purchase, Review
from schemas import CreateUser, ReadUser, ReadProduct, ReadTag
from database import SessionLocal
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from starlette.staticfiles import StaticFiles

app = FastAPI()
app.mount('/assets', StaticFiles(directory='visuals/assets'), name='assets')
templates = Jinja2Templates(directory="visuals")

load_dotenv()
reset_pass_signature = os.getenv('RESET_PASSWORD_SIGNATURE')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def does_username_exist(username: str, db: Session):
    if db.query(User).filter(User.username == username).first():
        raise HTTPException(status_code=400, detail="Username already exists")


def is_logged_in(db: Session, 
                 request: Request,
                 logged_id: str | None = Cookie(default=None)):
    if logged_id is None:
        return False
    user = db.get(User, int(logged_id))
    if user is None:
        return False
    return True


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    products = db.query(Product).all()
    context = {"products": products}
    return templates.TemplateResponse(request=request, name="home.html", context=context)


@app.get('/login')
def login(username: str, password: str, response: Response, db: Session = Depends(get_db)):
    user = db.scalars(select(User.id).where(User.username == username,
                                            User.password == password)).first()
    if user is not None:
        response.set_cookie(key = "logged_id", value = str(user))
        return {'Login Successful': True}, RedirectResponse("http://127.0.0.1:8000/")
    else:
        raise HTTPException(status_code=404, detail="Invalid username or password. Try again.")


@app.get('/logout')
def logout(response: Response):
    response.delete_cookie(key = "logged_id")
    return {'Logout Successful': True}


@app.post('/signup')
def create_user(new_user: CreateUser, db: Session = Depends(get_db)):
    does_username_exist(new_user.username, db)
    user = User(username=new_user.username, email=new_user.email, password=new_user.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.get('/user_profile', response_class=HTMLResponse)
def read_user(request: Request,
              logged_id : str | None = Cookie(default=None, include_in_schema=False),
              db: Session = Depends(get_db)):
    if not is_logged_in(db, request, logged_id):
        return templates.TemplateResponse(request=request, name="login.html")
    user = db.query(User).filter(User.id == logged_id).first()
    context = {"user": user}
    return templates.TemplateResponse(request=request, name="user_profile.html", context=context)


@app.get('/reset_password')
def reset_password(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if user:
        payload = {"user_id": user.id,
                   "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=10)}
        token = jwt.encode(payload=payload, key=reset_pass_signature,algorithm="HS256")
        return {"message:": 'Sent email to reset password if the user exists.',
                "To: ": user.email,
                "Reset Link: ": "http://127.0.0.1:8000/change_password?token=" + token}
    return {'Sent email to reset password if the user exists.'}


@app.put('/change_password')
def change_password(new_password: str,
                    logged_id: str | None = Cookie(default=None, include_in_schema=False),
                    token: str | None = '',
                    db: Session = Depends(get_db)):
    uid = logged_id
    if uid is None:
        try:
            decoded = jwt.decode(token, key=reset_pass_signature,
                                 algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=404, detail="Expired reset link, request a new one.")
        uid = decoded["user_id"]
    user = db.get(User, int(uid))
    user.password = new_password
    db.commit()
    db.refresh(user)
    return {'Successfully changed password.'}


@app.put('/change_username')
def change_username(username: str,
                    request: Request,
                    logged_id: str | None = Cookie(default=None, include_in_schema=False),
                    db: Session = Depends(get_db)):
    if not is_logged_in(db, request, logged_id):
        return templates.TemplateResponse(request=request, name="login.html")
    existing_name = db.query(User).filter(User.username == username).first()
    if existing_name is not None:
        raise HTTPException(status_code=404, detail="Username is taken. Select another one.")
    user = db.get(User, int(logged_id))
    user.username = username
    db.commit()
    return {'Successfully changed username.'}


@app.get('/wishlist', response_class=HTMLResponse)
def show_wishlist(request: Request,
                  logged_id : str | None = Cookie(default=None, include_in_schema=False),
                  db: Session = Depends(get_db)):
    if not is_logged_in(db, request, logged_id):
        return templates.TemplateResponse(request=request, name="login.html")
    wishlist = db.query(Wishlist.product_id).filter(Wishlist.user_id == int(logged_id)).all()
    return templates.TemplateResponse(request=request, name="wishlist.html", context={"wishlist": wishlist})


@app.put('/wishlist')
def add_to_wishlist(product_id: int,
                    request: Request,
                    logged_id: str | None = Cookie(default=None, include_in_schema=False),
                    db: Session = Depends(get_db)):
    if not is_logged_in(db, request, logged_id):
        return templates.TemplateResponse(request=request, name="login.html")
    product_in_wishlist = db.query(Wishlist).filter(Wishlist.product_id == product_id,
                                                 Wishlist.user_id == int(logged_id)).first()
    if product_in_wishlist is not None:
        raise HTTPException(status_code=404, detail="Product is already wishlisted.")
    product_in_purchases = db.query(Purchase).filter(Purchase.product_id == product_id,
                                                     Purchase.user_id == int(logged_id)).first()
    if product_in_purchases is not None:
        raise HTTPException(status_code=404, detail="You already own this product.")
    added_product = Wishlist(product_id=product_id, user_id=int(logged_id))
    db.add(added_product)
    db.commit()
    db.refresh(added_product)
    return {'Successfully added product to wishlist.'}


@app.delete('/wishlist')
def remove_from_wishlist(product_id: int,
                         request: Request,
                         logged_id: str | None = Cookie(default=None, include_in_schema=False),
                         db: Session = Depends(get_db)):
    if not is_logged_in(db, request, logged_id):
        return templates.TemplateResponse(request=request, name="login.html")
    product_in_wishlist = db.query(Wishlist).filter(Wishlist.product_id == product_id,
                                                    Wishlist.user_id == int(logged_id)).first()
    if product_in_wishlist is None:
        raise HTTPException(status_code=404, detail="Product is not in the wishlist.")
    db.delete(product_in_wishlist)
    db.commit()
    return {'Successfully removed product from wishlist.'}


@app.get('/cart', response_class=HTMLResponse)
def show_cart(request: Request,
              logged_id : str | None = Cookie(default=None, include_in_schema=False),
              db: Session = Depends(get_db)):
    if not is_logged_in(db, request, logged_id):
        return templates.TemplateResponse(request=request, name="login.html")
    cart = db.query(Cart).filter(Cart.user_id == int(logged_id)).all()
    return templates.TemplateResponse(request=request, name="cart.html", context={"cart": cart})


@app.put('/cart')
def add_to_cart(product_id: int,
                request: Request,
                logged_id : str | None = Cookie(default=None, include_in_schema=False),
                db: Session = Depends(get_db)):
    if not is_logged_in(db, request, logged_id):
        return templates.TemplateResponse(request=request, name="login.html")
    product_in_cart = db.query(Cart).filter(Cart.product_id == product_id,
                                            Cart.user_id == int(logged_id)).first()
    if product_in_cart is not None:
        raise HTTPException(status_code=404, detail="Product is already in the cart.")
    product_in_purchases = db.query(Purchase).filter(Purchase.product_id == product_id,
                                                     Purchase.user_id == int(logged_id)).first()
    if product_in_purchases is not None:
        raise HTTPException(status_code=404, detail="You already own this product.")
    added_product = Cart(product_id=product_id, user_id=int(logged_id))
    db.add(added_product)
    db.commit()
    db.refresh(added_product)
    return {'message': 'Successfully added product to cart.'}


@app.delete('/cart')
def remove_from_cart(product_id: int,
                     request: Request,
                     logged_id : str | None = Cookie(default=None, include_in_schema=False),
                     db: Session = Depends(get_db)):
    if not is_logged_in(db, request, logged_id):
        return templates.TemplateResponse(request=request, name="login.html")
    product_in_cart = db.query(Cart).filter(Cart.product_id == product_id,
                                            Cart.user_id == int(logged_id)).first()
    if product_in_cart is None:
        raise HTTPException(status_code=404, detail="Product is not in the cart.")
    db.delete(product_in_cart)
    db.commit()
    return {'message': 'Successfully removed product from cart.'}


@app.get('/products/{product_id}')
def get_product(product_id: int,
                logged_id : str | None = Cookie(default=None, include_in_schema=False),
                db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found.")
    product_info = {
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "discount": product.discount,
        "short_description": product.short_description,
        "full_description": product.full_description,
        "image_url": product.img_path
    }
    if logged_id is None:
        return {'product': product_info, 'write review': False}
    return {'product': product_info, 'write review': True}


@app.put('/products/{product_id}')
def add_review(product_id: int,
               review: str,
               review_recommendation: str,
               request: Request,
               logged_id : str | None = Cookie(default=None, include_in_schema=False),
               db: Session = Depends(get_db)):
    if not is_logged_in(db, request, logged_id):
        return templates.TemplateResponse(request=request, name="login.html")
    product = db.query(Product).filter(Product.id == product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found.")
    product_in_purchases = db.query(Purchase).filter(Purchase.product_id == product_id,
                                                     Purchase.user_id == int(logged_id)).first()
    if product_in_purchases is None:
        raise HTTPException(status_code=404, detail="Need to purchase the product before reviewing.")
    product_review = db.query(Review).filter(Review.product_id == product_id,
                                             Review.user_id == int(logged_id)).first()
    if product_review is None:
        product_review = Review(user_id=int(logged_id), product_id=product_id,
                                review_details=review, review_recommendation=review_recommendation,
                                review_date=func.current_date())
        db.add(product_review)
    else:
        product_review.review_details = review
        product_review.review_recommendation = review_recommendation
        product_review.review_date = func.current_date()
    db.commit()
    db.refresh(product_review)
    return 'Successfully reviewed the product.'


@app.post('/purchase')
def purchase_products(confirmation: bool,
                      request: Request,
                      logged_id : str | None = Cookie(default=None, include_in_schema=False),
                      db: Session = Depends(get_db)):
    if not is_logged_in(db, request, logged_id):
        return templates.TemplateResponse(request=request, name="login.html")
    if confirmation:
        cart = db.query(Cart).filter(Cart.user_id == int(logged_id)).all()
        if cart is None:
            raise HTTPException(status_code=404, detail="Cart is empty.")
        for cart_product in cart:
            purchased_product = Purchase(product_id=cart_product.product_id,user_id=int(logged_id),
                                         purchase_date=func.current_date())
            db.add(purchased_product)
            wishlisted_product = db.query(Wishlist).filter(Wishlist.user_id == int(logged_id),
                                                           Wishlist.product_id == cart_product.product_id).first()
            if wishlisted_product is not None:
                db.delete(wishlisted_product)
            db.delete(cart_product)
            db.commit()
            db.refresh(purchased_product)
        return {'Successfully purchased products.'}
    else:
        return {'Canceled transaction.'}


@app.get('/recommendations', response_class=HTMLResponse)
def show_recommendations(request: Request):
    return templates.TemplateResponse(request=request, name="recommendations.html",
                                      context={"request": request})