from pydantic import BaseModel,EmailStr,Field
from datetime import date


class InvoiceCreate(BaseModel):
    
    invoice_number : str = Field(min_length = 1)
    customer_name : str = Field(min_length = 1)
    customer_email : EmailStr
    invoice_date : date
    product_name : str = Field(min_length = 1)
    quantity : int = Field(gt=0)
    unit_price : float = Field(gt=0)


class InvoiceData(BaseModel):
    invoice_number : str = Field(min_length=1)
    customer_email : EmailStr
    invoice_date : date 
    customer_name : str = Field(min_length=1)
    product_name : str = Field(min_length=1)
    quantity : int = Field(gt=0)
    unit_price :float = Field(gt=0)
    discount_percentage : float = Field(ge=0, le=100)
    discount_amount : float  = Field(ge=0)
    tax_percentage : float = Field(ge=0, le=100)
    tax_amount : float =  Field(ge=0)
    subtotal : float = Field(ge=0)
    taxable_amount : float = Field(ge=0)
    total_amount : float = Field(ge=0)



class InvoicePatch(BaseModel):
    invoice_number : str | None = Field(default=None, min_length=1)
    customer_name : str | None =  Field(default=None, min_length=1)
    customer_email : EmailStr | None = None
    invoice_date : date | None = None
    product_name : str | None = Field(default=None, min_length=1)
    quantity : int | None = Field(default=None, gt=0)
    unit_price : float | None = Field(default=None, gt=0)



    