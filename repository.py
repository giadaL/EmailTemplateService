from uuid import UUID

from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

from database import SESSION
from models import EmailTemplates, Attachment


def find_all_templates() -> list[EmailTemplates]:
    return SESSION.query(EmailTemplates).all()


def find_all_attachments() -> list[Attachment]:
    return SESSION.query(Attachment).all()


def find_templates_by_id(tid: UUID):
    return SESSION.query(EmailTemplates).get(tid)


def find_attachment_by_id(aid: UUID):
    return SESSION.query(Attachment).get(aid)


def find_templates_by_name(name: str):
    return SESSION.query(EmailTemplates).filter_by(filename=func.lower(name)).first()


def find_attachments_by_template_id(tid: UUID) -> list[Attachment]:
    return SESSION.query(Attachment).filter_by(template_id=tid).all()


def _catch(function, errors, params=None) -> bool:
    res = False
    try:
        function(params)
        SESSION.commit()
        res = True
    except errors:
        res = False
    finally:
        SESSION.close()
        return res


def add_template(template: EmailTemplates) -> bool:
    return _catch(SESSION.add, SQLAlchemyError, template)


def add_all_templates(templates: EmailTemplates) -> bool:
    return _catch(SESSION.add_all, SQLAlchemyError, templates)


def add_attachment(attachment: Attachment) -> bool:
    return _catch(SESSION.add, SQLAlchemyError, attachment)


def add_all_attachments(attachments: list[Attachment]) -> bool:
    return _catch(SESSION.add_all, SQLAlchemyError, attachments)


def remove_template_by_id(tid):
    return _catch(SESSION.query(EmailTemplates).filter_by(id=tid).delete, SQLAlchemyError)


def remove_attachment_by_id(aid):
    return _catch(SESSION.query(Attachment).filter_by(id=aid).delete, SQLAlchemyError)
