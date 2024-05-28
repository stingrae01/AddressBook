# AddressBook
This repository is part of the Initial Coding Test for a fastapi developer.

## Overview of Task 
- Create an address book application where API users can create, update and delete addresses.
- The address should:
  - contain the coordinates of the address.
  - be saved to an SQLite database.
  - be validated
- API Users should also be able to retrieve the addresses that are within a given distance and
location coordinates.

## Installation
This project uses **python 3.7**. Ensure that you have the correct version.
1. Download a local copy of the repository by using this command:\
   ```git clone https://github.com/stingrae01/AddressBook.git```
2. Go to AddressBook folder.\
   ```cd AddressBook```
3. Setup a virtual environment to manage the dependencies.\
    ```python -m venv addressbook```
4. Activate the virtual environment\
    ```source addressbook/bin/activate```
5. Once the virtual environment is activated, install the dependencies. You can find them in the *requirements.txt* \
    ```pip install -r requirements.txt```
6. Set the environment variables. You can change the values as you wish, but to make the tests simpler, use these default values for the meantime.
    ```
    export ADDRESS_BOOK_API_KEY=af594db1058629e02cc37015f1dc612af582a23bb7bac34c01faff147b3663ad
    export ADDRESS_BOOK_DATABASE_URL=sqlite:///./address_book.db
    ```
7. Run the command below to start the server. This will run the application in port 8000.\
    `uvicorn main:app --host 0.0.0.0 --port 8000`
8. When the server has started, visit the documentation page to see all the end points available.\
http://localhost:8000/docs
9. Use the `API_KEY` that you set in **Step 6** when making requests from the endpoints.