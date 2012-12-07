# Politmus API
#### Prototype Web Service API for Politmus.

The prototype API is written in Python and runs on Google App Engine. There is a live version of the code, including documentation, running on [http://politmus-api.appspot.com](http://politmus-api.appspot.com).

The prototype does not implement any of the authentication features stated in the documentation. Please do not use this to collect real or potentially sensitive data.

#### Local Development

To run the prototype API locally follow these steps.

* Download the [Google App Engine SDK for Python](https://developers.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python) and ensure you install the command-line tools
* Clone the [politmus-api](https://github.com/ahume/politmus-api) Git repository
* `> cd politmus-api/`
* `> dev_appserver.py --use_sqlite app`

This will start the server on [http://localhost:8080](http://localhost:8080). Hit that URL to check it is working - it should redirect you to the documentation pages.

#### Importing Data

Sample data is included in the `fixtures` directory. You can import this data by requesting the following endpoints.

* Import user account data: [http://localhost:8080/import/users](http://localhost:8080/import/users)
* Import questions and MP data: [http://localhost:8080/import/mpvotes](http://localhost:8080/import/mpvotes) (this may take a few minutes to return!).


#### Run the tests

At this point you should be able to run the project's unit tests.

* `> python test/test.py`

