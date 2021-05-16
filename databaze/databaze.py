from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

SQLITE = 'sqlite'
MYSQL = 'mysql'
Base = declarative_base()


class Solider(Base):
    __tablename__ = 'solider'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=50))


class Db:
    DB_ENGINE = {
        SQLITE: 'sqlite:///{DB}',
        MYSQL: 'mysql+mysqlconnector://{USERNAME}:{PASSWORD}@localhost/{DB}'
    }

    def __init__(self, dbtype='sqlite', username='', password='', dbname='soliders'):
        dbtype = dbtype.lower()

        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname, USERNAME=username, PASSWORD=password)
            self.engine = create_engine(engine_url, echo=False)
        else:
            print('dont workin')

        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def read_all(self, order = Solider.name):
        try:
            result = self.session.query(Solider).order_by(order).all()
            return result
        except:
            return False

    def read_by_id(self, id):
        try:
            result = self.session.query(Solider).get(id)
            return result
        except:
            return False

    def create(self, solider):
        try:
            self.session.add(solider)
            self.session.commit()
            return True
        except:
            return False

    def update(self):
        try:
            self.session.commit()
            return True
        except:
            return False

    def delete(self, id):
        try:
            solider = self.read_by_id(id)
            self.session.delete(solider)
            self.session.commit()
            return True
        except:
            return False


