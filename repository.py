from uuid import UUID

from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from models import EmailTemplate, Attachment


def find_all_templates(session) -> list[EmailTemplate]:
    return session.query(EmailTemplate).all()


def find_all_attachments(session) -> list[Attachment]:
    return session.query(Attachment).all()


def find_templates_by_id(tid: UUID, session):
    return session.query(EmailTemplate).get(tid)


def find_attachment_by_id(aid: UUID, session):
    return session.query(Attachment).get(aid)


def find_template_by_name(name: str, session):
    return session.query(EmailTemplate).filter_by(filename=func.lower(name)).first()


def find_attachments_by_template_id(tid: UUID, session) -> list[Attachment]:
    return session.query(Attachment).filter_by(template_id=tid).all()


def _catch(function, errors, session, params=None, ) -> (bool, str):
    res = None
    error = None
    try:
        function(params)
        session.commit()
        res = True
    except IntegrityError:
        session.rollback()
        res = False
        error = '{ "message": "invalid field , duplicate key"}'
    except errors as e:
        session.rollback()
        res = False
        error = str(e)
    finally:
        session.close()
        print(res)
        return res, error


def add_template(template: EmailTemplate, session) -> (bool, str):
    return _catch(session.add, SQLAlchemyError, session, template)


def add_all_templates(templates: EmailTemplate, session) -> (bool, str):
    return _catch(session.add_all, SQLAlchemyError, session, templates)


def add_attachment(attachment: Attachment, session) -> (bool, str):
    return _catch(session.add, SQLAlchemyError, session, attachment)


def add_all_attachments(attachments: list[Attachment], session) -> (bool, str):
    return _catch(session.add_all, SQLAlchemyError, session, attachments)


def remove_template_by_id(tid, session):
    return _catch(session.query(EmailTemplate).filter_by(id=tid).delete, SQLAlchemyError, session)


def remove_attachment_by_id(aid, session):
    return _catch(session.query(Attachment).filter_by(id=aid).delete, SQLAlchemyError, session)
