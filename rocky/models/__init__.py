"""
Michael duPont - michael@mdupont.com
rocky.models
"""

# pylint: disable=E1101

from rocky import app, db

class NoIDMixin:
    __table_args__ = {'extend_existing': True}

    @classmethod
    def create(cls, commit: bool=True, **kwargs) -> 'self':
        """Adds a new instance to the database"""
        instance = cls(**kwargs)
        return instance.save(commit=commit)

    def update(self, commit: bool=True, **kwargs) -> 'bool/self':
        """Updates an instances values
        Returns bool if update successful or self if commit=False
        """
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit: bool=True) -> 'bool/self':
        """Save any changes to the database
        Returns bool if update successful or self if commit=False
        """
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit: bool=True) -> bool:
        """Deletes an instance from the database"""
        db.session.delete(self)
        return commit and db.session.commit()

class CRUDMixin(NoIDMixin):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    def get_id(self) -> str:
        """Return the object's ID as a string"""
        return str(self.id)

    @classmethod
    def get(cls, id: int) -> 'self':
        """Returns an instance by ID"""
        return cls.query.get(id)

    @classmethod
    def get_or_404(cls, id: int) -> 'self':
        """Returns an instance by ID or raises a 404 error"""
        return cls.query.get_or_404(id)

from rocky.models.user import User
