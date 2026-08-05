from fastapi import FastAPI, Depends, HTTPException, Cookie, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import user

from models import User, Wishlist
from schemas import CreateUser, ReadUser, ReadProduct, ReadTag

from database import SessionLocal

import secrets

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

'''def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()'''


@app.get("/")
async def root():
    return {"message": "API is running"}


'''@app.post("/users")
async def create_user(user: CreateUser, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    new_user = User(username=user.username, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(user)
    return new_user'''

users = \
    {1: [
        'rex', # 0 name
        'a',   # 1 password
        [1],   # 2 wishlist
        [],    # 3 cart
        {},    # 4 reviews
        [],    # 5 purchases
        'rex23@email.com' # 6 email
    ]} # id : [name, password, wishlist, cart, review, purchases, email]
logged_user = [None]
products = {1: ['appple', {1: 'great'}]}


password_reset_tokens = {}


user_db = {
    1: {
        "id": 1,
        "username": "rex",
        "hashed_password": "hashedpassa",
    },
    2: {
        "id": 2,
        "username": "zero",
        "hashed_password": "hashedpass0",
    }
}


@app.post('/users')
def create_user(user: CreateUser):
    u_id = len(users)+1
    users[u_id] = [user.username, user.password, [], [], {}, [], [], user.email]
    return {'user_id': u_id, 'username': user.username, 'password': user.password, 'email': user.email}


@app.get('/users/{user_id}')
def read_user(user_id: int, logged_id : str | None = Cookie(default=None)):
    if user_id not in users.keys():
        raise HTTPException(status_code=404, detail="User not found")
    return {'user_id': user_id, 'username': users[user_id][0]}


@app.get('/reset_password')
def reset_password(username: str):
    for key in users.keys():
        if users[key][0] == username:
            token = secrets.token_urlsafe(32)
            password_reset_tokens[key] = token
            reset_link = "http://127.0.0.1:8000/change_password?token=" + token
            print(f"To: {users[key][6]}")
            print(f"Link to reset password: {reset_link}")
            break
    return {'Sent email to reset password if the user exists.'}


@app.put('/change_password')
def change_password(new_password: str, logged_id: str | None = Cookie(default=None), token: str | None = ''):
    uid = logged_id
    if logged_id is None:
        for key in password_reset_tokens.keys():
            if token == password_reset_tokens[key]:
                uid = key
                password_reset_tokens.pop(key)
                break
        if uid is None:
            raise HTTPException(status_code=404, detail="Invalid or expired reset link. "
                                                        "Need to request password reset.")
    users[int(uid)][1] = new_password
    return {'Successfully changed password.'}


'''@app.put('/users/{user_id}')
def update_user(user_id: int, user: CreateUser, logged_id : str | None = Cookie(default=None)):
    if user_id not in users.keys():
        raise HTTPException(status_code=404, detail="User not found")
    users[user_id] = [user.username, user.password]
    return {'user_id': user_id, 'username': user.username, 'password': user.password}
'''

@app.get('/login')
def login(username: str, password: str, response: Response):
    user_val = [username, password]
    for key in users.keys():
        if users[key][0] == user_val[0] and users[key][1] == user_val[1]:
            response.set_cookie(key = "logged_id", value = str(key))
            return {'Login Successful': True}
    raise HTTPException(status_code=404, detail="Invalid username or password. Try again.")


@app.get('/logout')
def logout(response: Response):
    response.delete_cookie(key = "logged_id")
    return {'Logout Successful': True}


@app.get('/wishlist')
def show_wishlist(logged_id : str | None = Cookie(default=None)):
    if logged_id is None:
        raise HTTPException(status_code=404, detail="Not logged in.")
    return {'wishlist': users[int(logged_id)][2]}


@app.put('/wishlist')
def add_to_wishlist(product_id: int, logged_id : str | None = Cookie(default=None)):
    if logged_id is None:
        raise HTTPException(status_code=404, detail="Not logged in.")
    if product_id in users[int(logged_id)][2]:
        raise HTTPException(status_code=404, detail="Product is already wishlisted.")
    users[int(logged_id)][2].append(product_id)
    return {'Successfully added product to wishlist.'
            '\nwishlist': users[int(logged_id)][2]}


@app.delete('/wishlist')
def remove_from_wishlist(product_id: int, logged_id : str | None = Cookie(default=None)):
    if logged_id is None:
        raise HTTPException(status_code=404, detail="Not logged in.")
    if product_id not in users[int(logged_id)][2]:
        raise HTTPException(status_code=404, detail="Product is not in the wishlist.")
    users[int(logged_id)][2].remove(product_id)
    return {'Successfully removed product from wishlist.'
            '\nwishlist': users[int(logged_id)][2]}


@app.get('/cart')
def show_cart(logged_id : str | None = Cookie(default=None)):
    if logged_id is None:
        raise HTTPException(status_code=404, detail="Not logged in.")
    return {'cart': users[int(logged_id)][3]}


@app.put('/cart')
def add_to_cart(product_id: int, logged_id : str | None = Cookie(default=None)):
    if logged_id is None:
        raise HTTPException(status_code=404, detail="Not logged in.")
    if product_id in users[int(logged_id)][3]:
        raise HTTPException(status_code=404, detail="Product is already in the cart.")
    users[int(logged_id)][3].append(product_id)
    return {'Successfully added product from cart.'
            'cart': users[int(logged_id)][3]}


@app.delete('/cart')
def remove_from_cart(product_id: int, logged_id : str | None = Cookie(default=None)):
    if logged_id is None:
        raise HTTPException(status_code=404, detail="Not logged in.")
    if product_id not in users[int(logged_id)][3]:
        raise HTTPException(status_code=404, detail="Product is not in the cart.")
    users[int(logged_id)][3].remove(product_id)
    return {'Successfully removed product from cart.'
            'cart': users[int(logged_id)][3]}


@app.get('/products/{product_id}')
def get_product(product_id: int, logged_id : str | None = Cookie(default=None)):
    if product_id not in products.keys():
        raise HTTPException(status_code=404, detail="Product not found.")
    if logged_id is None:
        return {'product': products[product_id], 'write review': False}
    return {'product': products[product_id], 'write review': True}


@app.put('/products/{product_id}')
def add_review(product_id: int, review: str, logged_id : str | None = Cookie(default=None)):
    if logged_id is None:
        raise HTTPException(status_code=404, detail="Not logged in.")
    if product_id not in products.keys():
        raise HTTPException(status_code=404, detail="Product not found.")
    if product_id not in users[int(logged_id)][5]:
        raise HTTPException(status_code=404, detail="Need to purchase the product before reviewing.")
    products[product_id][1][int(logged_id)] = review
    users[int(logged_id)][4][product_id] = review
    return 'Successfully reviewed the product.'


@app.post('/purchase')
def purchase_products(confirmation: bool, logged_id : str | None = Cookie(default=None)):
    if logged_id is None:
        raise HTTPException(status_code=404, detail="Not logged in.")
    if not users[int(logged_id)][3]:
        raise HTTPException(status_code=404, detail="Cart is empty.")
    if confirmation:
        for product in users[int(logged_id)][3]:
            users[int(logged_id)][5].append(product)
            if product in users[int(logged_id)][2]:
                users[int(logged_id)][2].remove(product)
        users[int(logged_id)][3] = []
        return {'Successfully purchased products.'}
    else:
        return {'Canceled transaction.'}


'''@app.get('/login_authenticate')
def login_authenticate(token : str = Depends(oauth2_scheme)):
    return {'token': token}


def decode_auth_token(token: str):
    return ReadUser(id=9, username=token+"pluto")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = decode_auth_token(token)
    return user


@app.get('/users/me')
async def read_current_user(current_user: str = Depends(get_current_user)):
    return current_user


def fake_hash_password(password: str):
    return "hashedpass" + password'''


'''@app.post('/change password')
def change_password(username: str|None, password: str):
    if logged_user[0]:
        users[logged_user[0]][1] = password
        return {'Successfully changed password.'}
    else:
        if username in user'''
