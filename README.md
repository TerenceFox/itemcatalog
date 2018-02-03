# Udacity Full Stack Nanodegree Item Catalog Project

The goal of this project is to provide an understanding of CRUD operations with a server-side SQL database. The user flow begins at the index page, which shows all of the categories currently in the database and up to three of the most recently added items. Cards show information on categories and items. Click on the categories show all of the items that belong to it. Logging in with Google Sign-in allows a user to create new categories and new items. They can also edit their existing categories and items, but only if they're the original creator.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

This application was written in Python 2.7.12 and requires Python to run. See the installation instructions below for dealing with dependencies.

### Installing

To get this application running in an development environment:

Clone this repository or download it directly.

```
git clone https://github.com/TerenceFox/itemcatalog
```

A `requirements.txt` file is provided with all of the dependencies. Navigate to the root directory of the repo in the command line and run

```
pip install -r requirements.txt
```

To run the application, use the following commands from the root directory of the repo:

```
export FLASK_APP=catalog.py
flask run
```
Note: Google Sign-in expects the URL to be `http://localhost:5000`, the default address and port for Flask, and will reject a login request otherwise.

If you're running this application inside a virtual machine, you need to change the host address to make it visible to the rest of the network (such as your host machine). Use the option `--host="0.0.0.0"` with the `flask run` command.


##User Flow For The Web App

The database starts out empty. Sign in with Google to create a new user. Once signed in, you can create new categories. Once you've created a category, click on it to see the items page for it. Create items within the category. Categories can be edited and deleted from the index page, and items can be edited and deleted from the category page. Categories and items not created by the currently signed-in user will be viewable but not editable.

## Built With

* [Flask](http://flask.pocoo.org/docs/0.12/) - The web framework used
* [Flask-WTF](https://flask-wtf.readthedocs.io/en/stable/) - Extension for handling forms with WTForms
* [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/) - Extension for handling SQLAlchemy ORM

## Author

* **Terence Fox**


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Miguel Grinberg's [Flask Megatutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) was super helpful for modularizing the app and providing instruction on using WTForms.
* [Material Design](https://material.io/) was loosely followed for the styling of this project. Icons are Google Icon Font, typography is Roboto.
