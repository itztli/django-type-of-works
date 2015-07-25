from django.db.models.fields import CharField
from django.utils.encoding import  force_text,force_unicode
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class TypeOfWork(object):
    
    def __str__(self):
        return force_text(self.code or '')
    
    def __init__(self, code):
        self.code = code
    
    def __eq__(self, other):
        return force_text(self) == force_text(other or '')

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(force_text(self))

    def __repr__(self):
        if self.flag_url is None:
            repr_text = "{0}(code={1})"
        else:
            repr_text = "{0}(code={1}, flag_url={2})"
        return repr_text.format(
            self.__class__.__name__, repr(self.code), repr(self.flag_url))

    def __bool__(self):
        return bool(self.code)

    __nonzero__ = __bool__   # Python 2 compatibility.

    def __len__(self):
        return len(force_text(self))

    
    
    def __unicode__(self):
        return force_unicode(self.code or u'')

    def __eq__(self, other):
        return unicode(self) == force_unicode(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __cmp__(self, other):
        return cmp(unicode(self), force_unicode(other))

    def __hash__(self):
        return hash(unicode(self))

    def __repr__(self):
        return "%s(code=%r)" % (self.__class__.__name__, unicode(self))

    def __nonzero__(self):
        return bool(self.code)

    def __len__(self):
        return len(unicode(self))
    
    @property
    def name(self):
        # Local import so the countries aren't loaded unless they are needed. 
        from django_type_of_works.works import WORKS
        for code, name in WORKS:
            if self.code == code:
                return name
        return ''



class TypeOfWorkDescriptor(object):
    """
    A descriptor for country fields on a model instance. Returns a Country when
    accessed so you can do stuff like::

        >>> instance.country.name
        u'New Zealand'
        
        >>> instance.country.flag
        '/static/flags/nz.gif'
    """
    def __init__(self, field):
        self.field = field

    def __get__(self, instance=None, owner=None):
        if instance is None:
            raise AttributeError(
                "The '%s' attribute can only be accessed from %s instances."
                % (self.field.name, owner.__name__))
        return TypeOfWork(code=instance.__dict__[self.field.name])

    def __set__(self, instance, value):
        if value is not None:
            value = force_unicode(value)
        instance.__dict__[self.field.name] = value



class TypeOfWorkField(CharField):
    """
    A country field for Django models that provides all ISO 3166-1 countries as
    choices.
    
    """
    descriptor_class = TypeOfWorkDescriptor
 
    def __init__(self, *args, **kwargs):
        # Local import so the countries aren't loaded unless they are needed. 
        from django_type_of_works.works import WORKS
        #from django_countries.countries import COUNTRIES 

        kwargs.setdefault('max_length', 2) 
        kwargs.setdefault('choices', WORKS) 

        super(CharField, self).__init__(*args, **kwargs) 

    def get_internal_type(self): 
        return "CharField"

    def contribute_to_class(self, cls, name):
        super(TypeOfWorkField, self).contribute_to_class(cls, name)
        setattr(cls, self.name, self.descriptor_class(self))

    def get_prep_lookup(self, lookup_type, value):
        if hasattr(value, 'code'):
            value = value.code
        return super(TypeOfWorkField, self).get_prep_lookup(lookup_type, value)

    def pre_save(self, *args, **kwargs):
        "Returns field's value just before saving."
        value = super(CharField, self).pre_save(*args, **kwargs)
        return self.get_prep_value(value)

    def get_prep_value(self, value):
        "Returns field's value prepared for saving into a database."
        # Convert the Country to unicode for database insertion.
        if value is None:
            return None
        return unicode(value)


# If south is installed, ensure that CountryField will be introspected just
# like a normal CharField.
try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['^django_type_of_works\.fields\.TypeOfWorkField'])
except ImportError:
    pass