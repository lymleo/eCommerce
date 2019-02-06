# Checkout Process

1. Cart -> Checkout View
    ?
    - Login or Enter an Email(as Guest)
    - Shipping Address
    - Billing Info
        - Billing Address
        - Credit Cart / Payments

2. Billing App/Component
    - Billing Profile
        - User or Email (Guest Email)
        - generate paynment processor token(Strip or Braintee)

3. Orders / Invoices Component
    - Connecting the Billing Profile
    - Shilling / Billing adrress
    - Cart
    - Status -- Shipped? Cancelled?

4. backup fixtures
py manage.py dumpdata products --format json --indent 4 > products/fixtures/products.json