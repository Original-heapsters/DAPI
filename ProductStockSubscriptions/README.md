# Product Stock Subscriptions
> Imagine email subscriptions, but you actually cared

## Technologies
  - Front End
    - React + Redux
  - Back End
    - Python Flask
  - CI/CD
    - Tests + deployment will be done with github actions
  - Deployment
    - Frontend will be hosted via github pages under /DAPI/StockSub
    - Backend will be deployed to a heroku container

## Pitch
  What if you only wanted to be notified when an item of interest is in stock? You may not care about the most recent spring sale, but you want to know when that hyper-exclusive can of beer is restocked!
  With {NAME TBD} you just provide the best way to be notified, a link to the product you want to track, and an optional time frame to check stock. If no time frame is provided, it will be checked at 9am every morning.

## System Design
  - Front end
    The front end will include two phases. The first phase is a simple form with contact info, product info, and scheduler. With this info, the application can work as prescribed. The second phase will include accounts, with accounts you can have a dashboard of all the products youre tracking and manage your subscriptions if you go wild tracking too many products.
  - Back end
    The back end api will require one main endpoint `POST /track` with encrypted body parameters from the front end. Given the product link, we can use an html parser like beautifulsoup combined with a regex against common 'out of stock' phrases to determine if an item is back in stock. It is much easier to check for out of stock phrases rather than in stock because if an item is in stock there is not usually an idicator for that. Once a product is determined to be in stock, a notify method will be called. Items within the database will be short lived for the sake of storage space. For the time being a default of 30 days will be used for TTL's on objects. Once a successful notification goes out, the related database objects will be deleted
