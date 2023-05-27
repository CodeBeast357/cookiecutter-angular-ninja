# Generic UI / API

This is a generic setup for is a website for building out a website with an API deployed in kubernetes.  Really though right now this is some bare bones implementation stuff.

Items in the to do list: 

* Create migrations!

## Getting Started

### Install Tilt

```
curl -fsSL https://raw.githubusercontent.com/tilt-dev/tilt/master/scripts/install.sh | bash
```

### Git'er Done

```
tilt up
```
## Default locations

### Admin UI
Once you've got things started up, you should be able to reach the admin UI at http://ad-hoc.localhost/admin/

![Admin UI](img/admin_ui.png?raw=true)

### Angular UI
Once you've got things started up, you should be able to reach the admin UI at http://ad-hoc.localhost/ui/

![Admin UI](img/angular_ui.png?raw=true)

### Django Ninja Swagger Docs
Once you've got things started up, you should be able to reach the admin UI at http://ad-hoc.localhost/api/docs/

![Admin UI](img/api_docs.png?raw=true)


TO run a jupyter notebook: 

```
python -m venv venv
source venv/bin/activate
pip install -r ./generic_api/requirements.txt
AD_HOC_ENVIRONMENT=jupyter ./generic_api/generic_api/manage.py shell_plus --lab
```