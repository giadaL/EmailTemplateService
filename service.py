from base64 import b64decode

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models import EmailTemplate
from repository import save_template, find_template_by_name, find_templates_by_id, find_attachments_by_id_in, \
    save_all_attachments, remove_attachments_by_id_in
from schemas import CreateTemplateDTO, TemplateDTO, UpdateTemplateDTO


def create_template(template: CreateTemplateDTO, session: Session):
    file = b64decode(template.base64)
    template_to_save = EmailTemplate(template=file,
                                     subject=template.subject,
                                     filename=template.filename)
    response, error = save_template(template_to_save, session)

    if response:
        saved = find_template_by_name(template.filename, session)
        return TemplateDTO(id=saved.id,
                           subject=saved.subject,
                           attachments=saved.attachments,
                           filename=saved.filename), None

    session.close()
    return None, error


def update_template(template: UpdateTemplateDTO, session):
    template_db = find_templates_by_id(template.id, session)

    attachments = find_attachments_by_id_in(template.attachments, session)
    try:
        template_db.filename = template.filename
        template_db.subject = template.subject
        template_db.attachments = attachments
    except IntegrityError:
        session.rollback()
        session.close()
        return None, '{"message":"invalid filename, already exist"}'

    for at in attachments:
        at.template_id = template.id

    att_to_remove = list(filter(lambda att: not attachments.__contains__(att), template_db.attachments))
    if att_to_remove:
        res, error = remove_attachments_by_id_in(att_to_remove, session)

        if error or not res:
            return None, error

    res, error = save_all_attachments(attachments, session)
    if error or not res:
        return None, error

    res, error = save_template(template_db, session)
    if error or not res:
        return None, error

    return TemplateDTO(id=template_db.id, subject=template_db.subject, filename=template_db.filename,
                       attachments=attachments), None


def remove_template():
    pass
    # TODO


def get_all_templates():
    pass
    # TODO


def get_template_by_name():
    pass
    # TODO
