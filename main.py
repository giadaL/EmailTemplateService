from fastapi import FastAPI, Response

app = FastAPI()


@app.post("/template")
async def create_template() -> Response:
    """
    save template on db
    """
    # TODO


@app.put("/template")
async def update_template() -> Response:
    """
    update existing template by name
    """
    # TODO


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
