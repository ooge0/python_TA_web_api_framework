ADR-003: Pydantic v2 for API models
=====================================

**Status:** Accepted

**Context.** The original project used ``@dataclass`` models with hand-written
``from_dict()`` / ``to_dict()`` methods.  These were error-prone: nested models
were not recursively serialised, optional fields had no validation, and the
conversion logic was duplicated per class.

**Decision.** I replaced the dataclass models with pydantic v2 ``BaseModel``
subclasses.  Fields use pydantic's type coercion and validation.  Serialisation
is ``model.model_dump()``; deserialisation is ``Model(**dict)``.

**Consequences.** Models validate on construction — a bad payload fails
immediately with a clear error instead of producing a half-populated object.
``to_dict`` / ``from_dict`` boilerplate is gone.  The trade-off: pydantic is a
heavier dependency, and camelCase API fields require either ``alias`` or
``model_config = ConfigDict(populate_by_name=True)``.
