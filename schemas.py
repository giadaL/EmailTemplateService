from uuid import UUID

from pydantic import BaseModel


class CreateTemplateDTO(BaseModel):
    base64: str
    subject: str
    filename: str


class UpdateTemplateDTO(BaseModel):
    id: UUID
    subject: str
    attachments: list[UUID]
    filename: str


class TemplateInfoDTO(BaseModel):
    id: UUID
    subject: str
    attachments: list[UUID]
    filename: str


class CreateAttachmentDTO(BaseModel):
    base64: str
    filename: str
    mimetype: str
    template_id: UUID


class AttachmentDTO(BaseModel):
    id: UUID
    filename: str
    template_id: UUID
    base64: str
    mimetype: str


class TemplateDTO(BaseModel):
    base64: str
    filename: str
    id: UUID
