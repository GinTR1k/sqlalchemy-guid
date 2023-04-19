# sqlalchemy GUID

This is a simple extension to SQLAlchemy that adds support for UUID with 
postgresql compatibility to other database dialects.

## Installation

    pip install sqlalchemy_guid

## Usage

Basically, you just need to import the GUID type and use it in your models:

        import uuid
        from sqlalchemy.ext.declarative import declarative_base
        from sqlalchemy import Column, Integer
        from sqlalchemy_guid import GUID
    
        Base = declarative_base()
    
        class User(Base):
            __tablename__ = 'users'
            id = Column(Integer, primary_key=True)
            guid = Column(GUID, default=uuid.uuid4)

For postgresql it will use the native uuid type, for other database dialects it will use a CHAR(32), storing as stringified hex values.

Now, when you create a new user, the guid will be automatically generated:

        user = User()
        session.add(user)
        session.commit()
        print(user.guid)

It will also work with other database dialects, such as sqlite:

        from sqlalchemy import create_engine
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)

        session = Session(engine)
        user = User()
        session.add(user)
        session.commit()
        print(user.guid)

More sqlite examples can be found in the [tests](tests).

## License

[MIT](LICENSE)
