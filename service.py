from base64 import b64decode
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models import EmailTemplate, Attachment
from repository import save_template, find_template_by_name, find_all_templates, find_templates_by_id, \
    find_attachments_by_id_in, \
    save_all_attachments, remove_attachments_by_id_in, remove_template_by_id, save_attachment
from schemas import CreateTemplateDTO, TemplateDTO, UpdateTemplateDTO, CreateAttachmentDTO, AttachmentDTO


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

    session.close()
    return TemplateDTO(id=template_db.id, subject=template_db.subject, filename=template_db.filename,
                       attachments=attachments), None


def remove_template(template_id: UUID, session: Session) -> (bool, str):
    template  = find_templates_by_id(template_id, session)
    res, err = remove_attachments_by_id_in([at.id for at in template.attachments], session)
    if res:
        res = remove_template_by_id(template_id, session)

    session.close()
    return res


def get_all_templates(session: Session) -> list[TemplateDTO]:
    templates = find_all_templates(session)

    def remap_templates(template: EmailTemplate):
        attachs = [at.id for at in template.attachments]
        return TemplateDTO(id=template.id, subject=template.subject, attachments=attachs, filename=template.filename)

    session.close()
    return list(map(remap_templates, templates))


def get_template_by_id(template_id: UUID, session: Session) -> TemplateDTO:
    template = find_templates_by_id(template_id, session)
    session.close()

    return TemplateDTO(id=template.id, subject=template.subject, filename=template.filename,
                       attachments=[at.id for at in template.attachments]) if template else None


def upload_attachment(template_id: UUID, attachment_dto: CreateAttachmentDTO, session: Session):
    file = b64decode(attachment_dto.base64)
    attachment_to_save = Attachment(filename=attachment_dto.filename, mimetype=attachment_dto.mimetype,
                                    template_id=template_id, file=file)
    res, err = save_attachment(attachment_to_save, session)
    if res:
        template = find_templates_by_id(template_id, session)
        if template:
            attach = list(
                filter(lambda at: at.filename == attachment_dto.filename and at.mimetype == attachment_dto.mimetype,
                       template.attachments))
            if attach:
                session.close()
                att = attach[0]
                return AttachmentDTO(id=att.id, filename=att.filename, template_id=att.template_id), None
    session.close()
    return None, err
