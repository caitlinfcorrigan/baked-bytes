# Baked Bytes
Buy byte-sized pick-me-ups from Baked Bytes. Baked Bytes sells made-to-order baked goods, meaning customers can "buy" treats in a variety of flavor combinations and quantities, like a dozen vanilla cupcakes with chocolate frosting or a sugar cookie with pink frosting and sprinkles.

Baked Bytes uses Postgres for its menu and order history.

## Technologies Used
* Lanaguages: HTML, CSS, Python
* Frameworks: Django
* Authentication: 
* Data Model: PostgreSQL
* APIs: Stripe (https://stripe.com/docs/checkout/embedded/quickstart?lang=python)

## Entity Relationship Diagram (ERD)
![ERD](ERD.png)

## Wireframes

## RESTful Routing Chart
| HTTP METHOD (_Verb_) | URL (_Nouns_)     | CRUD    | Response          | Notes        |
| -------------------- | ----------------- | ------- | ----------------- | ------------ |
| GET | `/auth/google` | READ | Directs to Google login | |


## User Stories
- [ ] AAU, I want to view available bakery items.
- [ ] AAU, I want to add items to my cart.
- [ ] AAU, I want to purchase items in my cart.
- [ ] AAU, I want to view my order history.
- [ ] AAU, I want to login/logout.
- [ ] AAU, I want to create an account.
- [ ] AAU,
- [ ] AAU,
- [ ] AAU,

## MVP Goals
- [ ] Users can create an account.
- [ ] Users can login and log out.
- [ ] Users can view items available for purchase.
- [ ] Logged in users can view their order history.
- [ ] Logged in users can add items to their cart.
- [ ] Logged in users can "purchase" items in their cart.
- [ ] 
- [ ] 

## Stretch Goals (in order of priority)
- [ ] Logged in users can pay for their purchase using Stripe API.
- [ ] Users can create unique combinations of flavors (ex - vanilla cake with chocolate icing).
- [ ] Additonal forms of authentication (ex - OAuth or JWT)
- [ ] 
- [ ] 

## Sprints
* Thursday:
    - [ ] Create product/order tables in database
    - [ ] Seed database with products
    - [ ] Create Bytes (products) page
* Friday:
    - [ ] Implement Django authentication
    - [ ] Relate Users to Orders table
    - [ ] Begin styling pages
* Saturday:
    - [ ] Add Cart functionality
    - [ ] Practice Stripe API tutorial
* Sunday:
    - [ ] Implement checkout
    - [ ] More styling
* Monday:
    - [ ] Implement Stripe API
    - [ ] Finish any coding related to payments/checkout
* Tuesday:
    - [ ] Handle roadblocks / feature overflow
    - [ ] 
* Wednesday:
    - [ ] Finalize/clean up code



