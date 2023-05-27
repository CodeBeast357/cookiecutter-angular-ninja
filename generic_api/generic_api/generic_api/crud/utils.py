from asgiref.sync import sync_to_async
from django.shortcuts import get_object_or_404  # type: ignore
from django.db.models import ForeignKey
from django.db.models import Model
from django.db.models.fields.related_descriptors import ForeignKeyDeferredAttribute
from typing import List, Any, Dict
from ninja.orm import create_schema
from ninja import Router
from ninja.pagination import paginate, PageNumberPagination
from ninja.security import django_auth

import logging

LOGGER = logging.getLogger(__name__)

def _parse_fk_payload_keys(model: Model, payload_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Parse foreign key attributes from the payload dict to use against deferred fk attributes."""
    parsed_dict = {}
    for key, val in payload_dict.items():
        id_key = f'{key}_id'
        deferred_attr = getattr(model, id_key, None)
        if deferred_attr and isinstance(deferred_attr, ForeignKeyDeferredAttribute):
            parsed_dict[id_key] = val
        else:
            parsed_dict[key] = val
    return parsed_dict


def _get_model_router(model: Model, name: str) -> Router:
    LOGGER.debug("Doing the logging debug thing")

    router = Router()

    ModelPost = create_schema(model=model, name=f"CRUD{name.title()}Post", exclude=["id"])
    ModelGet = create_schema(model=model, name=f"CRUD{name.title()}Get")

    @router.post(f"/", operation_id=f"create_instance_{name}", summary=f"Create a new {model.__name__} instance from the given payload.")
    async def create_instance(request, payload: ModelPost):
        """Create a new instance based on input."""
        parsed_dict = _parse_fk_payload_keys(model, payload.dict())
        LOGGER.debug("Creating %s instance from parsed_dict %s", model.__name__, parsed_dict)
        instance = await sync_to_async(model.objects.create)(**parsed_dict)
        LOGGER.debug("Created %s instance %s", model.__name__, instance)
        return ModelGet.from_orm(instance)

    @router.get(f"/" + "{model_id}", response=ModelGet, operation_id=f"get_instance_{name}", summary=f"Return an {model.__name__} instance for the given id.")
    async def get_instance(request, model_id: int):
        """Return an instance for the ID specified."""
        instance = await sync_to_async(get_object_or_404)(model, id=model_id)
        return ModelGet.from_orm(instance)

    # TODO: Figure out how to get async pagination working because this is meh.
    @router.get(f"/", response=List[ModelGet], operation_id=f"list_instances_{name}", summary=f"Return a list of all {model.__name__} instances.")
    @paginate(PageNumberPagination)
    def list_instances(request):
        """Return a list of all model instances."""
        return model.objects.all()

    @router.put(f"/" + "{model_id}", operation_id=f"update_instance_{name}", summary=f"Update the {model.__name__} instance with the payload for the given id.")
    async def update_instance(request, model_id: int, payload: ModelPost):
        """Update the model instance with the payload."""
        instance = await sync_to_async(get_object_or_404)(model, id=model_id)
        parsed_dict = _parse_fk_payload_keys(model, payload.dict())
        for attr, value in parsed_dict.items():
            setattr(instance, attr, value)
        await sync_to_async(instance.save)()
        return ModelGet.from_orm(instance)

    @router.patch(f"/" + "{model_id}", operation_id=f"patch_instance_{name}", summary=f"Patch the {model.__name__} instance with the payload for the given id.")
    async def patch_instance(request, model_id: int, payload: ModelPost):
        """Update the model instance with the payload."""
        LOGGER.info("Patching model ID %s", model_id)
        instance = await sync_to_async(get_object_or_404)(model, id=model_id)
        parsed_dict = _parse_fk_payload_keys(model, payload.dict())
        for attr, value in parsed_dict.items():
            setattr(instance, attr, value)
        await sync_to_async(instance.save)()
        return ModelGet.from_orm(instance)

    @router.delete(f"/" + "{model_id}", operation_id=f"delete_instance_{name}", summary=f"Delete the {model.__name__} instance for the given id.")
    async def delete_instance(request, model_id: int):
        """Delete the model instance."""
        LOGGER.info("Deleting model ID %s", model_id)
        instance = await sync_to_async(get_object_or_404)(model, id=model_id)
        await sync_to_async(instance.delete)()
        return {"success": True}

    LOGGER.debug("Confingured router for %s", name)

    return router


def add_model_crud_route(api, name, model, auth=None):
    """Add a deafult crud router with url `name` for model `model` to the api."""
    LOGGER.info("Adding model CRUD route for model %s under name %s", model.__name__, name)
    api.add_router(f"/{name}/", _get_model_router(model, name), tags=[name], auth=auth)
