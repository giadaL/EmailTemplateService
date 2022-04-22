import uuid

from sqlalchemy import Column, String, DateTime, LargeBinary, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

_Base = declarative_base()


class EmailTemplate(_Base):
    __tablename__ = 'templates'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String, nullable=False, index=True, unique=True)
    template = Column(LargeBinary, nullable=False)
    subject = Column(String, nullable=False)
    attachments = relationship("Attachment", lazy='subquery')

    loaded = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return "<EmailTemplate(filename='{}',subject='{}', template='{}', loaded={}, attachments={})>" \
            .format(self.filename, self.subject, self.template, self.loaded, self.attachments)


class Attachment(_Base):
    __tablename__ = 'attachments'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String, nullable=False, index=True)
    file = Column(LargeBinary, nullable=False)
    mimetype = Column(String, nullable=False)
    template_id = Column(UUID(as_uuid=True), ForeignKey("templates.id"), nullable=False)

    def __repr__(self):
        return "<Attachment(filename='{}', file='{}', mimeType={}, template_id={})>" \
            .format(self.filename, self.file, self.mimetype, self.email_id)


def db_create_all(engine):
    _Base.metadata.create_all(engine)
