# Dumstigram
> Imagine instagram but random filters were applied to all the uploaded pictures

## Technologies
  - Front End
    - React + Redux
  - Back End
    - Python Flask
  - CI/CD
    - Tests + deployment will be done with github actions
  - Deployment
    - Frontend will be hosted via github pages under /DAPI/dumstigram
    - Backend will be deployed to a shared heroku container

## Pitch
  Are you tired of seeing the same old instragram post with the perfectly tailored pictures? Why not spice it up with a random filter(s) against your will? Nuke the image? Laser eyes? Space background? Who knows what you will get!

## System Design
  - Front end
    The front end will have three aspects. A user account management section, a feed, and an upload screen. The feed will need to support both logged in and guest users, the difference will be a more curated feed for logged in users with random accounts sprinkled in as well. The upload screen is meant to be as minimal as possible, there should be no capability to edit a picture prior to or after upload.
  - Back end
    The backend will be done in python since opencv has optimal image editing capabilities. There will be a flask api to support backend routing and the filters will be individual classes that adhere to a strict format. Given an input picture, identify key aspects if necessary, perform filter/edit, return image.
