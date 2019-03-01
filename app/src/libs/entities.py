import re

from sqlalchemy import String, Column, Date, inspect, DateTime, Integer
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.ext.declarative import declared_attr


@as_declarative()
class Base:
    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class MixinEntity:
    pattern_class_name_to_table_name = re.compile("[A-Z][^A-Z]*")

    @declared_attr
    def __tablename__(cls):
        split_res = re.findall(__class__.pattern_class_name_to_table_name, cls.__name__)
        return '_'.join(split_res).lower()


class VisitStat(Base, MixinEntity):
    uid = Column(String, primary_key=True)
    date_visit = Column(Date)
    time_visit = Column(DateTime)
    timestamp = Column(Integer)
    project = Column(String)
    path = Column(String)
    request_ip = Column(String)
    user_agent = Column(String)
