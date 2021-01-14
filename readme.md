# Iran-ATCA

this project is created to serve as a website for Iran-ATCA (Iranian Air Traffic Controllers Association).
in this project multiple consepts in django development are covered and the project contains the following parts(apps):

1. Blog

   to provide a blog app, in order to handle `Posts` and `Comments`.

2. Company

   the main model to handle information about Organization itself and some other models for consepts related to the Organization.

3. Custom

   in order to override and provide more Customization over Django default apps and templates.

4. Documents

   assuming as a library app. DocumentApp is used to provide features to have a library and in the future a book-store (but not only including the books).

5. Forum

   a forum app. using `django-channels` and `websocket` capabilities to provide a chat and messaging application.

6. Users

   somehow could be included in `Custom App` but because it's about the `User` models and customization for that specific model, I decided to make this a separate app.

django third party packegs used in this project are listed in `requirements.txt` but for more details I'll mention below:

1. [django-jalali-date](https://github.com/a-roomana/django-jalali-date)

   Jalali Date support for user interface. Easy conversion of DateTimeFiled to JalaliDateTimeField within the admin site, view and templates.

2. [django-widget-tweaks](https://github.com/jazzband/django-widget-tweaks)

   Tweak the form field rendering in templates, not in python-level form definitions. Altering CSS classes and HTML attributes is supported.

3. [social-auth-app-django](https://github.com/python-social-auth/social-app-django)

   This is the Django component of the [python-social-auth](https://github.com/python-social-auth/social-core) ecosystem, it implements the needed functionality to integrate social-auth-core in a Django based project.

4. [django-ckeditor](https://github.com/django-ckeditor/django-ckeditor)

   Provides a RichTextField and CKEditorWidget utilizing CKEditor with image upload and browsing support included.

5. [django-modeltranslation](https://github.com/deschler/django-modeltranslation)

   The modeltranslation application is used to translate dynamic content of existing Django models to an arbitrary number of languages without having to change the original model classes. It uses a registration approach (comparable to Django's admin app) to be able to add translations to existing or new projects and is fully integrated into the Django admin backend.

6. [sorl-thumbnail](https://github.com/jazzband/sorl-thumbnail)

   sorl-thumbnail is a very useful package to deal with images in the Django template. It is very easy to implement. Resizing and cropping images become simple with inbuilt tags provided by sorl-thumbnail.

7. [django-social-share](https://github.com/fcurella/django-social-share)

   The Django Social Share in the one of the unique Feature or library in django that make very effiecient for us to make the social media share links with very easier and unique without any trouble to handle the posting the website link post on the social platform , by single click we can easily share the post on any socail media platform .

8. [django-avatar](https://github.com/grantmcconnaughey/django-avatar)

   Django-avatar is a reusable application for handling user avatars. It has the ability to default to Gravatar if no avatar is found for a certain user. Django-avatar automatically generates thumbnails and stores them to your default file storage backend for retrieval later.

9. [django-channels](https://github.com/django/channels/blob/1.x/docs/index.rst)

   Channels is a project to make Django able to handle more than just plain HTTP requests, including WebSockets and HTTP2, as well as the ability to run code after a response has been sent for things like thumbnailing or background calculation.

## Notice

- in order to make trigram similarity aviable, we need to make sure that an extension called pg_trgm is activated first in PostgreSQL, you can create this extension using SQL with `CREATE EXTENSION pg_trgm;` or create a data migration in Django(do both to make sure):

      from django.contrib.postgres.operations import TrigramExtension

      class Migration(migrations.Migration):
        ...

        operations = [
            TrigramExtension(),
            ...
        ]
