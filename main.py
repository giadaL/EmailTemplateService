from typing import List
from uuid import UUID

import uvicorn
from fastapi import FastAPI, Response, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

import service
from database import SESSION
from schemas import CreateTemplateDTO, UpdateTemplateDTO, TemplateInfoDTO, CreateAttachmentDTO, AttachmentDTO, \
    TemplateDTO

app = FastAPI()


@app.post("/template", response_model=TemplateInfoDTO)
def create_template(template: CreateTemplateDTO, session: Session = Depends(SESSION)):
    """
    save template on db
    """
    res, err = service.create_template(template, session)

    return res \
        if res \
        else Response(status_code=HTTP_400_BAD_REQUEST, content=err, media_type="application/json")


@app.put("/template", response_model=TemplateInfoDTO)
def update_template(template: UpdateTemplateDTO, session: Session = Depends(SESSION)) -> Response:
    """
    update existing template by id
    """
    res, err = service.update_template(template, session)

    return res \
        if res \
        else Response(status_code=HTTP_400_BAD_REQUEST, content=err, media_type="application/json")


@app.get("/template/{template_id}/info", response_model=TemplateInfoDTO)
def find_template(template_id: UUID, session: Session = Depends(SESSION)) -> Response:
    """
    get template info by id
    """
    res = service.get_template_info_by_id(template_id, session)

    return Response(status_code=HTTP_200_OK, content=res.json(), media_type="application/json") \
        if res \
        else Response(status_code=HTTP_404_NOT_FOUND, content="{}", media_type="application/json")


@app.get("/template/{template_name}", response_model=TemplateDTO)
def find_template_by_name(template_name: str, session: Session = Depends(SESSION)) -> Response:
    """
    get template by name
    """
    res = service.get_template_by_name(template_name, session)

    return Response(status_code=HTTP_200_OK, content=res.json(), media_type="application/json") \
        if res \
        else Response(status_code=HTTP_404_NOT_FOUND, content="{}", media_type="application/json")


@app.get("/templates/info", response_model=List[TemplateInfoDTO])
def find_all_templates(session: Session = Depends(SESSION)):
    """
    get all templates infos
    """
    res = service.get_all_templates(session)

    return res


@app.delete("/template/{template_id}")
def remove_template(template_id: UUID, session: Session = Depends(SESSION)):
    """
    remove template by id
    """
    res, error = service.remove_template(template_id, session)
    return Response(status_code=HTTP_200_OK,
                    content='{"message": "delete success"}', media_type="application/json") if res else Response(
        status_code=HTTP_409_CONFLICT,
        content='{"message": "something went wrong, can\'t delete" }', media_type="application/json")


@app.post("/template/{template_id}/attachment", response_model=AttachmentDTO)
def save_attachment(template_id: UUID, attachment: CreateAttachmentDTO, session: Session = Depends(SESSION)):
    """
    upload attachment and link  it to a template
    """
    res, err = service.upload_attachment(template_id, attachment, session)
    return res if res else Response(
        status_code=HTTP_400_BAD_REQUEST,
        content=err, media_type="application/json")


@app.get("/template/{template_id}/attachments", response_model=list[AttachmentDTO])
def get_attachments(template_id: UUID, session: Session = Depends(SESSION)):
    """
    upload attachment and link  it to a template
    """
    res, err = service.get_template_attachments(template_id, session)
    return res if res else Response(
        status_code=HTTP_400_BAD_REQUEST,
        content=err, media_type="application/json")


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, reload=True, access_log=False)
