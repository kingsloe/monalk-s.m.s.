from django.db import models

PAYMENT_METHOD = [
    ('Pay_Per_Day', 'Pay Per Day'),
    ('School_Fees_Aside', 'School Fees Aside'),
    ('Pay_Per_Term', 'Pay Per Term')

]

PAYMENT_CATEGORY = [
    ('Pay_Everything', 'Pay Everything'),
    ('Dont_Pay', 'Don\'t Pay'),
    ('Considered', 'Considered'),
]

FORM_OF_TRANSPORTATION = [
    ('Bus', 'Bus'),
    ('Walk', 'Walk')
]
