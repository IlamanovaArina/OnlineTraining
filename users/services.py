import stripe

from config import settings


# from config import settings


def create_stripe_product(product):
    """ Функция создания продукта для оплаты """
    stripe.api_key = settings.API_KEY
    # Создали продукт(курс) для оплаты
    stripe_product = stripe.Product.create(name=product.name,
                                           active=True,
                                           metadata={
                                               "description": product.description,
                                               "owner": product.owner,
                                               "price": product.price,
                                           }
                                           )
    return stripe_product


def modify_stripe_product(product):
    """ Функция обновления продукта для оплаты """
    stripe.api_key = settings.API_KEY
    # Создали продукт(курс) для оплаты
    return stripe.Product.modify(id=product.id_stripe_product,
                                 metadata={
                                     "description": product.description,
                                     "owner": product.owner,
                                     "price": product.price,
                                 }
                                 )


def create_stripe_price(price: int, id_stripe_product):
    """ Функция создания цены продукта для оплаты """
    stripe.api_key = settings.API_KEY
    # Создали цену
    return stripe.Price.create(currency='rub',
                               product=id_stripe_product,
                               unit_amount=price * 100
                               )


def create_stripe_session(price):
    stripe.api_key = settings.API_KEY
    """ Функция, которая открывает платёжную сессию. """
    session = stripe.checkout.Session.create(success_url="http://127.0.0.1:8000/",
                                    line_items=[{"price": price.get("id"), "quantity": 1}],
                                    mode='payment',
                                    )
    return session.get("id"), session.get("url")
