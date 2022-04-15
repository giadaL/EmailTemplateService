from base64 import b64decode

from sqlalchemy.orm import Session

from models import EmailTemplate
from repository import add_template, find_template_by_name
from schemas import CreateTemplateDTO, TemplateDTO


def create_template(template: CreateTemplateDTO, session: Session):
    file = b64decode(template.base64)
    template_to_save = EmailTemplate(template=file,
                                     subject=template.subject,
                                     filename=template.filename)
    response, error = add_template(template_to_save, session)

    if response:
        saved = find_template_by_name(template.filename, session)
        return TemplateDTO(id=saved.id,
                           subject=saved.subject,
                           attachments=saved.attachments,
                           filename=saved.filename), None

    return None, error


def update_template():
    pass
    # TODO


def remove_template():
    pass
    # TODO


def get_all_templates():
    pass
    # TODO


def get_template_by_name():
    pass
    # TODO
