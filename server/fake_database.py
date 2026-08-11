users = \
    {
        1: [                 # id
            'rex',            # 0 name
            'a',              # 1 password
            [],               # 2 wishlist
            [],               # 3 cart
            {1: 'great'},     # 4 reviews (product id, review)
            [1],              # 5 purchases
            'rex23@email.com' # 6 email
            ],
        2: [
            'Bash',
            'red3',
            [1],
            [],
            {},
            [],
            'rex23@email.com'
        ]
    } # id : [name, password, wishlist, cart, review, purchases, email]

products = {
    1: [                            # product id
        'The Talos Principle',      # Game name
        {
            1: 'great'              # User id, review
        }
    ]
}

password_reset_tokens = {}