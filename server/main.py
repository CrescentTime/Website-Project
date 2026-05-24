from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import user

from models import User, Wishlist
from schemas import CreateUser, ReadUser, ReadProduct, ReadTag

from database import SessionLocal

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
users = {1: ['rex', 'a', [1], [], {}, [], []]}
logged_user = [None]
products = {1: ['appple', {1: 'great'}]}

@app.post('/users')
def create_user(user: CreateUser):
    u_id = len(users)+1
    users[u_id] = [user.username, user.password]
    return {'user_id': u_id, 'username': user.username, 'password': user.password}


@app.get('/users/{user_id}')
def read_user(user_id: int, q: str|None = None):
    if user_id not in users.keys():
        raise HTTPException(status_code=404, detail="User not found")
    return {'user_id': user_id, 'username': users[user_id][0]}


@app.put('/users/{user_id}')
def update_user(user_id: int, user: CreateUser, q: str|None=None):
    if user_id not in users.keys():
        raise HTTPException(status_code=404, detail="User not found")
    users[user_id] = [user.username, user.password]
    return {'user_id': user_id, 'username': user.username, 'password': user.password}


@app.get('/login')
def login(username: str, password: str):
    user_val = [username, password]
    for key in users.keys():
        if users[key][0] == user_val[0] and users[key][1] == user_val[1]:
            logged_user.pop()
            logged_user.append(key)
            return {'Login Successful': True}
    raise HTTPException(status_code=404, detail="Invalid username or password. Try again.")


@app.get('/wishlist')
def show_wishlist():
    if logged_user[0] is None:
        raise HTTPException(status_code=404, detail="Not logged in.")
    return {'wishlist': users[logged_user[0]][2]}


@app.put('/wishlist')
def add_to_wishlist(product_id: int):
    if logged_user[0] is None:
        raise HTTPException(status_code=404, detail="Not logged in.")
    if product_id in users[logged_user[0]][2]:
        raise HTTPException(status_code=404, detail="Product is already wishlisted.")
    users[logged_user[0]][2].append(product_id)
    return {'Successfully added product to wishlist.'
            '\nwishlist': users[logged_user[0]][2]}


@app.delete('/wishlist')
def remove_from_wishlist(product_id: int):
    if logged_user[0] is None:
        raise HTTPException(status_code=404, detail="Not logged in.")
    if product_id not in users[logged_user[0]][2]:
        raise HTTPException(status_code=404, detail="Product is not in the wishlist.")
    users[logged_user[0]][2].remove(product_id)
    return {'Successfully removed product from wishlist.'
            '\nwishlist': users[logged_user[0]][2]}


@app.get('/cart')
def show_cart():
    if logged_user[0] is None:
        raise HTTPException(status_code=404, detail="Not logged in.")
    return {'cart': users[logged_user[0]][3]}


@app.put('/cart')
def add_to_cart(product_id: int):
    if logged_user[0] is None:
        raise HTTPException(status_code=404, detail="Not logged in.")
    if product_id in users[logged_user[0]][3]:
        raise HTTPException(status_code=404, detail="Product is already in the cart.")
    users[logged_user[0]][3].append(product_id)
    return {'Successfully added product from cart.'
            'cart': users[logged_user[0]][3]}


@app.delete('/cart')
def remove_from_cart(product_id: int):
    if logged_user[0] is None:
        raise HTTPException(status_code=404, detail="Not logged in.")
    if product_id not in users[logged_user[0]][3]:
        raise HTTPException(status_code=404, detail="Product is not in the cart.")
    users[logged_user[0]][3].remove(product_id)
    return {'Successfully removed product from cart.'
            'cart': users[logged_user[0]][3]}


@app.get('/products/{product_id}')
def get_product(product_id: int):
    if product_id not in products.keys():
        raise HTTPException(status_code=404, detail="Product not found.")
    if logged_user[0] is None:
        return {'product': products[product_id], 'write review': False}
    return {'product': products[product_id], 'write review': True}


@app.put('/products/{product_id}')
def add_review(product_id: int, review: str):
    if logged_user[0] is None:
        raise HTTPException(status_code=404, detail="Not logged in.")
    if product_id not in products.keys():
        raise HTTPException(status_code=404, detail="Product not found.")
    if product_id not in users[logged_user[0]][5]:
        raise HTTPException(status_code=404, detail="Need to purchase the product before reviewing.")
    products[product_id][1][logged_user[0]] = review
    users[logged_user[0]][4][product_id] = review
    return 'Successfully reviewed the product.'


@app.post('/purchase')
def purchase_products(confirmation: bool):
    if logged_user[0] is None:
        raise HTTPException(status_code=404, detail="Not logged in.")
    if not users[logged_user[0]][3]:
        raise HTTPException(status_code=404, detail="Cart is empty.")
    if confirmation:
        for product in users[logged_user[0]][3]:
            users[logged_user[0]][5].append(product)
            if product in users[logged_user[0]][2]:
                users[logged_user[0]][2].remove(product)
        users[logged_user[0]][3] = []
        return {'Successfully purchased products.'}
    else:
        return {'Canceled transaction.'}


