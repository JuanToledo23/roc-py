from sqlalchemy.orm import DeclarativeBase


def keyvalgen(obj):
    """Generates attr name/val pairs, filtering out SQLA attrs."""
    excl = ('_sa_adapter', '_sa_instance_state',)
    for k, v in vars(obj).items():
        if not k.startswith('_') and not any(hasattr(v, a) for a in excl):
            yield k, v


class Base(DeclarativeBase):
    def __repr__(self) -> str:
        params = ', '.join(f'{k}={v}' for k, v in keyvalgen(self))
        return f'{self.__class__.__name__}({params})'
