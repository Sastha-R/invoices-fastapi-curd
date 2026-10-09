from fastapi import FastAPI , Request
from fastapi.responses import JSONResponse
from routes.route import invoice_route
from exception.custom_exceptions import (InvoiceNotFoundError,InvoiceAlreadyExistsError)

app = FastAPI()
app.include_router(router = invoice_route)


@app.exception_handler(InvoiceNotFoundError)
def invoice_not_found_handler(request : Request,exc : InvoiceNotFoundError):
    return JSONResponse(status_code = 404,content={"msg" : str(exc)}) 

@app.exception_handler(InvoiceAlreadyExistsError)
def invoice_already_exist_handler(request : Request,exc : InvoiceAlreadyExistsError):
    return JSONResponse(status_code = 409,content={"msg" : str(exc)}) 

