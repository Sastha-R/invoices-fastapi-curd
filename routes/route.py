from schemas.schemas import InvoiceCreate,InvoicePatch
from fastapi import APIRouter,File,Form,UploadFile
from services.services import Services
from datetime import date
from typing import Annotated

services = Services()
invoice_route = APIRouter()

# @invoice_route.post("/invoices")
# async def create_invoices(invoices : InvoiceCreate):
#     return await services.create_invoice(invoices)


# @invoice_route.post("/invoices")
# async def create_invoices(
#     invoices: Annotated[InvoiceCreate, Form()],
#     photo: UploadFile = File(...)
# ):
#     return await services.create_invoice(invoices, photo)



@invoice_route.post("/invoices")
async def create_invoices(
    invoice_number: str = Form(...),
    customer_name: str = Form(...),
    customer_email: str = Form(...),
    invoice_date: date = Form(...),
    product_name: str = Form(...),
    quantity: int = Form(...),
    unit_price: float = Form(...),
    photo: UploadFile = File(...)
):
    invoices = InvoiceCreate(
        invoice_number=invoice_number,
        customer_name=customer_name,
        customer_email=customer_email,
        invoice_date=invoice_date,
        product_name=product_name,
        quantity=quantity,
        unit_price=unit_price
    )

    return await services.create_invoice(invoices, photo)

@invoice_route.get("/invoices")
async def get_invoices(limit : int = 10 , offset : int = 0):
    return await services.get_invoices(limit,offset)


@invoice_route.get("/invoices/{invoice_id}")
async def get_invoice_id(invoice_id : int):
        return await services.get_invoice_by_id(invoice_id)
   

@invoice_route.put("/invoices/{invoice_id}")
async def update_invoice(invoice_id : str,invoices : InvoiceCreate):
        return await services.update_invoice(invoice_id,invoices)


@invoice_route.patch("/invoices/{invoice_id}")
async def patch_invoice(invoice_id: str, invoice: InvoicePatch):

    return await services.patch_invoice(invoice_id, invoice)


@invoice_route.delete("/invoices/{invoice_id}")
async def delete_invoice(invoice_id : int):
    return await services.delete_invoice(invoice_id)
    


