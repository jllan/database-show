# -*- coding: utf-8 -*-
from flask.ext.sqlalchemy import SQLAlchemy
from config import TABLE_NAME
from create_app import app
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

db = SQLAlchemy(app)


class Event(db.Model):
    __tablename__ = TABLE_NAME
    ID = db.Column(db.Integer, primary_key = True)
    Itemid = db.Column(db.String(100))
    Sid = db.Column(db.String(100))
    ExpoName = db.Column(db.String(100))
    UnitCode = db.Column(db.String(100))
    UnitName = db.Column(db.String(100))
    #UnitNameEn = db.Column(db.String(100))
    CityName = db.Column(db.String(100))
    StartDate = db.Column(db.String(100))
    EndDate = db.Column(db.String(100))
    Site = db.Column(db.String(100))
    Exhibitor = db.Column(db.String(100))
    Visitor = db.Column(db.String(100))
    ExpoArea = db.Column(db.String(100))
    GetDate = db.Column(db.String(100))

    def __init__(self, itemid='', sid='', expo_name='', unit_code='', unit_name='', city_name='', start_date='', end_date='', site='', exhibitor='', visitor='', expo_area='', get_date=''):
        self.Itemid = itemid
        self.Sid = sid
        self.ExpoName = expo_name
        self.UnitCode = unit_code
        self.UnitName = unit_name
        #self.UnitNameEn = unit_name_en
        self.CityName = city_name
        self.StartDate = start_date
        self.EndDate = end_date
        self.Site = site
        self.Exhibitor = exhibitor
        self.Visitor = visitor
        self.ExpoArea = expo_area
        self.GetDate = get_date
