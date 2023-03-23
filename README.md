# Sherpa-Coding-Challenge

The following challenge was proposed by [Sherpa](https://www.sherpa.ai/).

I will use this README to talk about the decisions made and the reasoning behind them

## Installation and running

(Optional, recommended) Use `venv` first, with `python -m venv <name of your venv>`

To install all the requirements: `pip install -r /path/to/requirements.txt`

To run: `python -m src.app` or `python -m flask --app src/app.py run`

To execute tests: `pytest` or `python -m pytest` from the root folder

## Decisions

*Not necessarily in any order:*

1. Build a working version first, then clean up and refactor as needed.
   1. Perfection is the enemy of good. I find myself falling into this pitfall often, and this will help me avoid it.
2. Use venv
   1. It helps with Python modules (which can be a pain if not kept in check)
3. Use camelCase
   1. I prefer it over snake_case, although I could conform to either.
4. Used an id system instead of names for identifying users
      1. It is a bad practice (and I don't particularly like it either) to use names as the identifier, since they are by nature mutable, so I employed an id system instead.
      2. It is not written in the requirements, but there was no explicit prohibition either.
5. The route will be `user/:userId`
   1. This may seem counterintuitive given the desire to locate a user's city and update the DB, but it better allows the extension of this API easily without changing the existing functionality.
   2. It is preferable for REST API routes to be resources rather than actions, since those will come in the form of the HTTP action (`GET`, `PUT`, etc). What we do in each case should always be clearly documented and intuitive. Thus if we receive an `UPDATE` for a user, it's clear what to do.
   3. Only one endpoint is expected, not multiple, so even creating a user will go through this route (`PATCH`). This will therefore assume any end-users of this API will control that the id is correct. An alternative would be to use UUIDs or similar.
   4. How the parameters are received is also not specified. They could be URL params, or inside the request's body. I have assumed they'll come inside the body (except the `userId`, which will be in the URL) to follow common REST API practices.
   5. The main downside to this approach is that it won't work if it was ever decided that anything other than ids would follow the `/user` route (e.g. `/user/all`) as it would be interpreted as a `userId` as well
6. The return for `GET user/:userId` is not cleaned. It returns every item
   1. This is to avoid making a custom encoder and all the logic. It makes it cleaner and for the purposes of this challenge it should do
7. No input validation
   1. We assume our end-users are stakeholders/internal to our company and thus will make correct use of the API.
8. No modelling of the Geonames API
   1. It would be wise to wrap it so we know what to expect within the code but didn't have time.
9.  Use Flask
    1.  Although an implementation detail, it is a simpler and lighter framework than Django, can work perfectly for the stated requirements and one I've worked with in the past with no issues. If it's not broken, don't fix it (but keep questioning if it works)!
10. Use pytest
    1.  Another implementation detail. Simple and intuitive testing framework. Fits our needs.
    2.  Could use the built-in unittest but it isn't as easy to work with and pytest has widespread usage so all possible questions will be answered.
11. No security implemented
    1.  Simply due to a lack of time, but otherwise some form of authentication would've been implemented to avoid users being able to modify other users' profiles, unless explicitly desired
    2.  This could've come with a role-based system where admins could modify any users and many other possibilities, for example.
12. No logging
    1.  This would make the application hard to debug in case of errors. It should be done if it were to make it to production
13. No custom exceptions
    1.  They would take too much time and regular ones work for now. Would include in production
14. Local, in-memory DB
    1.  Nowhere is it specified which type of DB is expected, only that 2 tables are expected: 'Master' and 'Detalle'. I opted for a local version with a simple dictionary, although in production a proper DB would be used, wrapping the appropriate driver in our own class to only expose the methods we need, allowing for modularity and easy swapping in case we ever wanted to.
15. Use DDD as the goal
   1. It is the best Clean Architecture I have followed and the one I'm familiar with. It is easily scalable, clearly defined and modular.
16. Use the first item returned by the Geonames API
    1.  Without any further info like country code, I have no way to determine which result to pick from the array returned.
    2.  If more info was given, then we could filter/narrow the search.
17. Given-when-then test structure applied where possible
    1.  It is a good framework to work with when writing tests.
    2.  It provides a clear environment for each test of what exactly is being tested, and reduces cognitive load when reading them.
18. In the tests I imported `src` files despite not being the subject under test
    1.  They should've been mocks. However, I used them for the sake of time.
    2.  Never would this be shipped to production, as unit tests would no longer be reliable.
19. I made a `logic` file that can easily be broken into Use Cases, with an injectable DB for the sake of testability
    1.  That DB can be mocked, and should be an interface instead of a concrete implementation. This was done for the sake of time.
20. `User`s are value-objects since we treat them as equals even if they are different instances.
21. No `User` tests
    1.  The only "logic" is the equality one (initialisation is built-in), and is simple enough that it shouldn't require any testing.
22. Made the `PUT` operation be idempotent [as expected](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PUT).
23. In order to fulfil the TypeScript requirements I would require an actual DB or exposing the current one, essentially turning this app into a DBMS of sorts
    1.  Time constraints impeded it.
24. No ENV variables
    1.  Simply didn't deem it necessary for such a simple project.
    2.  I would've used them in production, however.
25. Testing the HTTP Requests themselves should be done via Postman or similar
    1.  Time constraints impeded mocking the DB properly with Flask.
    2.  All paths can be covered and automated.
    3.  The tests I included are not independent. Many use multiple HTTP calls to the same SUT.
26. All commits were made to the `main` branch for simplicity
    1.  In a real environment, each development would've had its branch and PR, with a ticket associated to it.
27. I would've liked to create a `ValueObject` and used it via Inheritance, but lacked the time so I just duplicated the `__eq__` functions.
    1.  A generic version, maybe comparing the two objects' being an instance of the same Class as well as having the same `__dict__` might-ve been a way to do so
28. No point creating a `SaveUserCriteria` as it would be the same as a `User`
29. No handling errors from the Geonames API. I assume our end-users will never reach the rate limit
30. I could've modeled Postal Codes, Names, IDs, Cities, but decided not to for the sake of simplicity
    1.  Usually it's a good idea to wrap them in custom classes, especially if we were to have specific logic for them such as UUIDs or parsing