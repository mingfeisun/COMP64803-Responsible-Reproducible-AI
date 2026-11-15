# Node Todo App

A Node app built with MongoDB and Angular. For demonstration purposes and a tutorial.

Node provides the RESTful API. Angular provides the frontend and accesses the API. MongoDB stores like a hoarder.

## Requirements

- [Node and npm](http://nodejs.org)
- MongoDB: Reminder that you will need an accompanying MongoDB container defined in your `docker-compose.yml` file under service 'database'.
The app will look for the database at hostname `database` and port 27017 (default MongoDB port)

## Installation

1. Clone the repository: `git clone https://github.com/0xcf/decal-sp18-a10.git`
2. Install the application: `npm install`
3. Start the server: `nodejs server.js`
4. If you do not run this using Docker Compose, this should fail because the server has been modified to expect a MongoDB instance at the hostname `database`, which you will set up as part of the lab!


Happy Todo-ing!

![Todo-aholic](http://i.imgur.com/ikyqgrn.png)
