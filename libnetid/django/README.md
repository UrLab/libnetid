# Django application for authenticating users with the `libnetid`

`libnetid.django` is a Django app that can be used to authenticate users with their netids.
It provides a custom (extensible) user model and a Django authentication backend.

It will soon provide some default views for login/logout and an admin app.

## Installation

* `pip install libnetid`
* add `libnetid.django` to your `INSTALLED_APPS`
* create a `User` model that subclasses `libnetid.django.models.AbstractNetidUser`
* set `AUTH_USER_MODEL = 'YourUserModel'` in your settings
* add `'libnetid.django.backends.NetidBackend'` to `AUTHENTICATION_BACKENDS` in your settings

## Configuration

You may configure this app with the `LIBNETID` variable in your settings. For example :

    LIBNETID = {
        'store_inscriptions': True,
    }

Available keys :
* `store_inscriptions` (bool) : store the user's inscriptions (like : IRCI1-polytech-2014) in the database.
* `exclude_privacy` (list of str) : data to explicitly remove from the database to protect users privacy. (TBD) (Optional, defaults to `[]`)


## Extend the provided User model

If the provided user model is too limited for your usecase, you may extend it. (abstract model TBD)
