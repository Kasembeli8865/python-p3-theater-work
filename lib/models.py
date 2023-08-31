from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create an SQLAlchemy engine and session
engine = create_engine('sqlite:///theater.db')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    character_name = Column(String())

    # Relationship to Auditions
    auditions = relationship('Audition', back_populates='role')

    def __repr__(self):
        return f'<Role {self.character_name}>'

    def actors(self):
        return [audition.actor for audition in self.auditions]

    def locations(self):
        return [audition.location for audition in self.auditions]

    def lead(self):
        hired_audition = next((audition for audition in self.auditions if audition.hired), None)
        if hired_audition:
            return hired_audition
        else:
            return "no actor has been hired for this role"

    def understudy(self):
        hired_auditions = [audition for audition in self.auditions if audition.hired]
        if len(hired_auditions) >= 2:
            return hired_auditions[1]
        else:
            return "no actor has been hired for understudy for this role"

class Audition(Base):
    __tablename__ = 'auditions'

    id = Column(Integer, primary_key=True)
    actor = Column(String())
    location = Column(String())
    hired = Column(Boolean, default=False)

    role_id = Column(Integer, ForeignKey('roles.id'))
    role = relationship('Role', back_populates='auditions')

    def __repr__(self):
        return f'<Audition {self.actor} for {self.role.character_name}>'

    def call_back(self):
        self.hired = True
        session.commit()
