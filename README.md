# Sherpa-Coding-Challenge

The following challenge was proposed by [Sherpa](https://www.sherpa.ai/).

I will use this README to talk about the decisions made and the reasoning behind them

## Decisions

1. Build a working version first, then clean up and refactor as needed.
   1. Perfection is the enemy of good. I find myself falling into this pitfall often, and this will help me avoid it.
2. Use venv
   1. It helps with Python modules (which can be a pain if not kept in check)
3. Use camelCase
   1. I prefer it over snake_case, although I could conform to either.
4. The route will be `user/:id`
   1. This may seem counterintuitive given the desire to locate a user's city and update the DB, but it better allows the extension of this API easily without changing the existing functionality.
   2. It is preferable for REST API routes to be resources rather than actions, since those will come in the form of the HTTP action (GET, PUT, etc). What we do in each case should always be clearly documented and intuitive. Thus if we receive an UPDATE for a user, it's clear what to do.
   3. I don't particularly like using the name as the identifier, so I employed an ID system. It is not written in the requirements, but there was no explicit prohibition, so I took the liberty to do so.
   4. How the parameters are received is also not specified. They could be URL params, or inside the request's body. I have assumed they'll come inside the body (except the ID, which will be in the URL) to follow common REST API practices.
