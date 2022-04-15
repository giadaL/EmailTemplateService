import json
from uuid import UUID

from psycopg2.errors import NotNullViolation, UniqueViolation
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

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


def find_attachments_by_id_in(attach_ids: list[UUID], session) -> list[Attachment]:
    return session.query(Attachment).filter(Attachment.id.in_(attach_ids)).all()


def _catch(function, errors, session, params=None, ) -> (bool, str):
    res = None
    error = None
    try:
        function(params)
        session.commit()

        res = True
    except UniqueViolation:
        res = False
        error = '{ "message": "invalid field , duplicate key"}'
        session.rollback()
        session.close()
    except NotNullViolation:
        res = False
        error = '{ "message": "invalid field ,cannot be null"}'
        session.rollback()
        session.close()
    except errors as e:
        res = False
        error = json.loads(e)

        session.rollback()
        session.close()
    except:
        res = False
        error = '{"message": "something went wrong"}'

        session.rollback()
        session.close()
    finally:
        return res, error


def save_template(template: EmailTemplate, session) -> (bool, str):
    return _catch(session.add, SQLAlchemyError, session, template)


def save_all_templates(templates: EmailTemplate, session) -> (bool, str):
    return _catch(session.add_all, SQLAlchemyError, session, templates)


def save_attachment(attachment: Attachment, session) -> (bool, str):
    return _catch(session.add, SQLAlchemyError, session, attachment)


def save_all_attachments(attachments: list[Attachment], session) -> (bool, str):
    return _catch(session.add_all, SQLAlchemyError, session, attachments)


def remove_template_by_id(tid, session):
    return _catch(session.query(EmailTemplate).filter_by(id=tid).delete(), SQLAlchemyError, session)


def remove_attachment_by_id(aid, session):
    return _catch(session.query(Attachment).filter_by(id=aid).delete(), SQLAlchemyError, session)


def remove_attachments_by_id_in(att_ids, session):
    return _catch(session.query(Attachment).filter(Attachment.id.in_(att_ids)).delete(), SQLAlchemyError, session)
