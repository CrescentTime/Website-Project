users = \
    {
        1: [                  # id
            'rex',            # 0 name
            'a',              # 1 password
            [],               # 2 wishlist
            [],               # 3 cart
            {                 # 4 reviews (product id, review)
                1: 'great'
            },
            [1],              # 5 purchases
            'rex23@email.com' # 6 email
        ],
        2: [
            'Bash',            # 0 name
            'Ray3',              # 1 password
            [2],               # 2 wishlist
            [4],               # 3 cart
            {                 # 4 reviews (product id, review)
                3: 'Could use more interesting puzzles'
            },
            [3],              # 5 purchases
            'rex23@email.com' # 6 email
        ]
    } # id : [name, password, wishlist, cart, review, purchases, email]

products = {
    1: [                            # product id
        'The Talos Principle',      # Game name
        {
            1: 'great'              # User id, review
        }
    ],
    2: [
        'Hades',
        {

        }
    ],
    3: [
        'God of War',
        {
            2: 'Could use more interesting puzzles'
        }
    ],
    4: [
        'Persona 3 Reload',
        {

        }
    ]
}

password_reset_tokens = {}