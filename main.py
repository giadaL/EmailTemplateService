from fastapi import FastAPI, Response, Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

import service
from database import SESSION
from schemas import CreateTemplateDTO, UpdateTemplateDTO

app = FastAPI()


@app.post("/template", response_class=ORJSONResponse)
async def create_template(template: CreateTemplateDTO, session: Session = Depends(SESSION)) -> Response:
    """
    save template on db
    """
    res, err = service.create_template(template, session)

    return Response(status_code=HTTP_200_OK, content=res.json(), media_type="application/json") \
        if res \
        else Response(status_code=HTTP_400_BAD_REQUEST, content=err, media_type="application/json")


@app.put("/template", response_class=ORJSONResponse)
async def update_template(template: UpdateTemplateDTO, session: Session = Depends(SESSION)) -> Response:
    """
    update existing template by id
    """
    res, err = service.update_template(template, session)

    return Response(status_code=HTTP_200_OK, content=res.json(), media_type="application/json") \
        if res \
        else Response(status_code=HTTP_400_BAD_REQUEST, content=err, media_type="application/json")


@app.get("/template")
async def find_template() -> Response:
    """
    get template by name
    """
    # TODO


@app.get("/templates")
async def find_all_templates() -> Response:
    """
    get all templates
    """
    # TODO


@app.delete("/template")
async def remove_template() -> Response:
    """
    remove template by name
    """
    # TODO


@app.post("/attachment")
async def save_attachment() -> Response:
    """
    upload attachment and link  it to a template
    """
    # TODO
