import uuid
from typing import Any, Optional, Type, Union

from sqlalchemy import CHAR, UUID, Dialect, TypeDecorator
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql.type_api import TypeEngine

_T = Type['_T']


class GUID(TypeDecorator):
    """Platform-independent GUID type.
    Uses PostgreSQL's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.
    """

    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect: Dialect) -> TypeEngine[Any]:
        if dialect == postgresql.dialect:
            return dialect.type_descriptor(UUID(as_uuid=True))
        return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value: Any, dialect: Dialect) -> Optional[str]:
        if value is None:
            return value
        if dialect == postgresql.dialect:
            return str(value)
        if not isinstance(value, uuid.UUID):
            return f'{uuid.UUID(value).int:032x}'
        return f'{value.int:032x}'

    @staticmethod
    def _uuid_value(value: _T) -> Union[uuid.UUID, _T]:
        if value is None:
            return value
        if not isinstance(value, uuid.UUID):
            value = uuid.UUID(value)
        return value

    def process_result_value(self, value: _T, dialect: Dialect) -> Union[uuid.UUID, _T]:
        return self._uuid_value(value)
