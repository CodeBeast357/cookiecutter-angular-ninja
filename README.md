# Generic UI / API

This is a generic setup for is a website for building out a website with an API deployed in kubernetes.  Really though right now this is some bare bones implementation stuff.

Items in the to do list: 

* Create utils to pull migrations from containers so they don't need to be built all hacky.

## Getting Started

### Install Tilt

```
curl -fsSL https://raw.githubusercontent.com/tilt-dev/tilt/master/scripts/install.sh | bash
```

### Git'er Done

If you want to develop on the cookiecutter template, you can use:

```
cookiecutter -f --no-input .
```

And then in the newly created directory:

```
tilt up
```

![Tilt Up](img/tilt-up.png?raw=true)

Any time you want to make an adjustment, you can rerun the cookiecutter command above to overwrite the files in place and tilt will automatically update
the deployments as necessary - this is useful if you want to add more services, etc.

## Default locations

### Admin UI
Once you've got things started up, you should be able to reach the admin UI at http://app.localhost/admin/

![Admin UI](img/django-admin.png?raw=true)

### Angular UI
Once you've got things started up, you should be able to reach the admin UI at http://app.localhost/ui/

![Angular UI](img/angular-ui.png?raw=true)

### Django Ninja Swagger Docs
Once you've got things started up, you should be able to reach the admin UI at http://app.localhost/api/docs/

![Swagger UI](img/swagger-docs.png?raw=true)


TO run a jupyter notebook: 

```
python -m venv venv
source venv/bin/activate
pip install -r ./generic_api/requirements.txt
AD_HOC_ENVIRONMENT=jupyter ./generic_api/generic_api/manage.py shell_plus --lab
```