from typing import List
from uuid import UUID

from fastapi import FastAPI, Response, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

import service
from database import SESSION
from schemas import CreateTemplateDTO, UpdateTemplateDTO, TemplateDTO

app = FastAPI()


@app.post("/template", response_model=TemplateDTO)
def create_template(template: CreateTemplateDTO, session: Session = Depends(SESSION)):
    """
    save template on db
    """
    res, err = service.create_template(template, session)

    return res \
        if res \
        else Response(status_code=HTTP_400_BAD_REQUEST, content=err, media_type="application/json")


@app.put("/template", response_model=TemplateDTO)
def update_template(template: UpdateTemplateDTO, session: Session = Depends(SESSION)) -> Response:
    """
    update existing template by id
    """
    res, err = service.update_template(template, session)

    return res \
        if res \
        else Response(status_code=HTTP_400_BAD_REQUEST, content=err, media_type="application/json")


@app.get("/template/{template_id}", response_model=TemplateDTO)
def find_template(template_id: UUID, session: Session = Depends(SESSION)) -> Response:
    """
    get template by id
    """
    res = service.get_template_by_id(template_id, session)

    return Response(status_code=HTTP_200_OK, content=res.json(), media_type="application/json") \
        if res \
        else Response(status_code=HTTP_404_NOT_FOUND, content="{}", media_type="application/json")


@app.get("/templates", response_model=List[TemplateDTO])
def find_all_templates(session: Session = Depends(SESSION)):
    """
    get all templates
    """
    res = service.get_all_templates(session)

    return res


@app.delete("/template")
def remove_template() -> Response:
    """
    remove template by name
    """
    # TODO


@app.post("/attachment")
def save_attachment() -> Response:
    """
    upload attachment and link  it to a template
    """
    # TODO
