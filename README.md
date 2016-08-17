# ingersollthreefive

TODO:
* Handle static files properly. (As part of deploy, change "../static" to "/static/" (Right now the static serving is probably not being done by nginx, so this should change)
* Setup the model/db (add app to InstalledApps in settings.py)
* setup admin user, etc.
* rearrange the templates dir to be "website/templates/website/home.html" so render can be called with "/website/home.html" to prevent future template name collisions.
