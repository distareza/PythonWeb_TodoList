# https://docs.sqlalchemy.org/en/14/orm/quickstart.html

from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, Boolean, Table, select, UniqueConstraint,join, MetaData
from sqlalchemy.orm import declarative_base, relationship, Session

Base = declarative_base()
metadata = MetaData()

class Master(Base):
    __tablename__ = "master"
    id = Column(Integer, primary_key=True)
    name = Column(String(250), unique=True, nullable=False)
    description = Column(String(1024))

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return f"id={self.id}, name={self.name}, description={self.description}"

class Detail(Base):
    __tablename__ = "detail"
    __table_args__ = ( UniqueConstraint('master_id', 'name'),  )
    id = Column(Integer, primary_key=True)
    master_id = Column(Integer, ForeignKey("master.id"))
    name = Column(String(250), nullable=False)
    complete = Column(Boolean)

    def __init__(self, parentId, name):
        self.master_id = parentId
        self.name = name
        self.complete = False

    def __repr__(self):
        return f"id={self.id}, name={self.name}, complete={self.complete}"

class Data():
    def __init__(self):
        self.connection = create_engine("sqlite:///todolist.db", echo=True)
        self.session = Session(self.connection)

    def create_db(self):
        Base.metadata.create_all(self.connection)

    def drop_db(self):
        Base.metadata.drop_all(self.connection)

    def getAllData(self):
        data = self.session.query(Master, Detail).where(Master.id == Detail.master_id)
        return [{
                    "List" : item.Master.name,
                    "todo" : item.Detail.name ,
                    "complete" : item.Detail.complete
                } for item in data ]

    def getAllMasterData(self):
        data = self.session.query(Master)
        return [{
            "id": item.id,
            "List" : item.name,
            "Description": item.description
        } for item in data]

    def getData(self, name:str):
        data = self.session.query(Master, Detail).where(Master.id == Detail.master_id, Master.name == name)
        return [{
                    "todo" : item.Detail.name ,
                    "complete" : item.Detail.complete
                } for item in data ]

    def addMasterData(self, name:str, description:str):
        master = Master(name, description)
        self.session.add(master)
        self.session.commit()

    def getMasterData(self, name:str):
        stmt = select(Master).where(Master.name == name)
        return self.session.scalar(stmt)

    def updateMasterData(self, name: str, description: str):
        master = self.getMasterData(name)
        if master is None:
            raise Exception(f"Could not found Todo {name}")
        master.description = description
        self.session.commit()

    def removeMasterData(self, name: str):
        master = self.getMasterData(name)
        if master is None:
            raise Exception(f"Could not found Todo {name}")

        self.removeDetailData(name)
        self.session.delete(master)
        self.session.commit()

    def addDetailData(self, name:str, todo:str):
        master = self.getMasterData(name)
        if master is None:
            raise Exception(f"Could not found Todo {name}")

        detail = Detail(master.id, todo)
        self.session.add(detail)
        self.session.commit()

    def removeDetailData(self, name:str):
        master = self.getMasterData(name)
        if master is None:
            raise Exception(f"Could not found Todo {name}")

        stmt = select(Detail).where(Detail.master_id == master.id)
        for detail in self.session.scalars(stmt):
            self.session.delete(detail)

    def getDetailData(self, name:str, todo:str):
        master = self.getMasterData(name)
        if master is None:
            raise Exception(f"Could not found Todo {name}")

        stmt = select(Detail).where(Detail.master_id == master.id).where(Detail.name == todo)
        return self.session.scalar(stmt)


    def getListData(self, parentId:int):
        stmt = select(Detail).where(Detail.master_id == parentId)
        data = self.session.scalars(stmt)
        return [{
            "id" : item.id,
            "name" : item.name,
            "complete": item.complete
        } for item in data]

    def updateDetail(self, id:int, flag:Boolean):
        data = self.session.scalar(select(Detail).where(Detail.id == id))
        if data is not None:
            data.complete = flag
            self.session.commit()


