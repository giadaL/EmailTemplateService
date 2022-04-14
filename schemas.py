from uuid import UUID


class CreateTemplateDTO:
    base64: str
    subject: str


class UpdateTemplateDTO:
    id: UUID
    subject: str
    attachments: list[UUID]


class TemplateDTO:
    id: UUID
    base64: str
    subject: str
    attachments: list[UUID]


class CreateAttachmentDTO:
    base64: str
    template_id: UUID


class AttachmentDTO:
    id: UUID
    base64: str
    template_id: str
