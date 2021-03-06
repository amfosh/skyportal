import datetime
from itertools import cycle, islice
import uuid
from tempfile import mkdtemp
import numpy as np
import factory
from skyportal.models import (DBSession, User, Group, Photometry,
                              Spectrum, Instrument, Telescope, Obj,
                              Comment, Thumbnail, Filter)

TMP_DIR = mkdtemp()


class BaseMeta:
    sqlalchemy_session = DBSession()
    sqlalchemy_session_persistence = 'commit'


class TelescopeFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta(BaseMeta):
        model = Telescope

    name = factory.LazyFunction(lambda: f'Palomar 48 inch_{str(uuid.uuid4())}')
    nickname = factory.LazyFunction(lambda: f'P48_{str(uuid.uuid4())}')
    lat = 33.3563
    lon = -116.8650
    elevation = 1712.
    diameter = 1.2


class CommentFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta(BaseMeta):
        model = Comment

    text = f'Test comment {str(uuid.uuid4())}'
    ctype = 'text'
    author = 'test factory'


class InstrumentFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta(BaseMeta):
        model = Instrument

    name = factory.LazyFunction(lambda: f'ZTF_{str(uuid.uuid4())}')
    type = 'Imager'
    band = 'Optical'
    telescope = factory.SubFactory(TelescopeFactory)
    filters = ['ztfg', 'ztfr', 'ztfi']


class PhotometryFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta(BaseMeta):
        model = Photometry

    instrument = factory.SubFactory(InstrumentFactory)
    mjd = factory.LazyFunction(lambda: 58000. + np.random.random())
    flux = factory.LazyFunction(lambda: 20 + 10 * np.random.random())
    fluxerr = factory.LazyFunction(lambda: 2 * np.random.random())


class ThumbnailFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta(BaseMeta):
        model = Thumbnail

    type = 'new'


class SpectrumFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta(BaseMeta):
        model = Spectrum

    instrument = factory.SubFactory(InstrumentFactory)
    wavelengths = np.sort(1000 * np.random.random(10))
    fluxes = 1e-9 * np.random.random(len(wavelengths))
    observed_at = datetime.datetime.now()


class GroupFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta(BaseMeta):
        model = Group
    name = factory.LazyFunction(lambda: str(uuid.uuid4()))
    users = []


class FilterFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta(BaseMeta):
        model = Filter
    query_string = str(uuid.uuid4())


class ObjFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta(BaseMeta):
        model = Obj
    id = factory.LazyFunction(lambda: str(uuid.uuid4()))
    ra = 0.0
    dec = 0.0
    redshift = 0.0
    altdata = {"simbad": {"class": "RRLyr"}}

    @factory.post_generation
    def groups(obj, create, passed_groups, *args, **kwargs):
        if not passed_groups:
            passed_groups = []
        instruments = [InstrumentFactory(), InstrumentFactory()]
        filters = ['ztfg', 'ztfr', 'ztfi']
        for instrument, filter in islice(zip(cycle(instruments), cycle(filters)), 10):
            np.random.seed()
            phot1 = PhotometryFactory(obj_id=obj.id,
                                      instrument=instrument,
                                      filter=filter,
                                      groups=passed_groups,
                                      alert_id=np.random.randint(100, 9223372036854775807))
            DBSession().add(phot1)
            DBSession().add(PhotometryFactory(obj_id=obj.id, flux=99.,
                                              fluxerr=99.,
                                              instrument=instrument,
                                              filter=filter,
                                              groups=passed_groups,
                                              alert_id=np.random.randint(100, 9223372036854775807)))

            DBSession().add(ThumbnailFactory(photometry=phot1))
            DBSession().add(CommentFactory(obj_id=obj.id, groups=passed_groups))
        DBSession().add(SpectrumFactory(obj_id=obj.id,
                                        instrument=instruments[0]))
        DBSession().commit()


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta(BaseMeta):
        model = User

    username = factory.LazyFunction(lambda: f'{uuid.uuid4()}@cesium-ml.org')

    @factory.post_generation
    def roles(obj, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for role in extracted:
                obj.roles.append(role)
                DBSession().add(obj)
                DBSession().commit()

    @factory.post_generation
    def groups(obj, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for group in extracted:
                obj.groups.append(group)
                DBSession().add(obj)
                DBSession().commit()
