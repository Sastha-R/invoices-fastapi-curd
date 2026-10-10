from repository.repository import Repository
from schemas.schemas import InvoiceData,InvoicePatch
from exception.custom_exceptions import (InvoiceNotFoundError,InvoiceAlreadyExistsError)
from utilities.file_handler import (FileHandler,PRODUCT_PHOTO_FOLDER,DELIVERY_PROOF_FOLDER)

class Services:

    def __init__(self):
        self.repository = Repository()
        self.filehandler = FileHandler()

    async def create_invoice(self, invoice , photo):

        existing_invoice = await self.repository.get_by_invoice_number(invoice.invoice_number)

        if  existing_invoice:
            raise InvoiceAlreadyExistsError("Invoice number already exists")


        subtotal = invoice.quantity * invoice.unit_price
        if subtotal < 10000:
            discount_percentage = 5
        elif subtotal <= 50000:
            discount_percentage = 10
        else:
            discount_percentage = 15

        discount_amount = subtotal * discount_percentage / 100

        taxable_amount = subtotal - discount_amount

        tax_percentage = 18

        tax_amount = taxable_amount * tax_percentage / 100

        total_amount = taxable_amount + tax_amount
        
        invoice_data = InvoiceData(
            invoice_number=invoice.invoice_number,
            customer_email=invoice.customer_email,
            invoice_date=invoice.invoice_date,
            customer_name=invoice.customer_name,
            product_name=invoice.product_name,
            quantity=invoice.quantity,
            unit_price=invoice.unit_price,
            discount_percentage=discount_percentage,
            discount_amount=discount_amount,
            tax_percentage=tax_percentage,
            tax_amount=tax_amount,
            subtotal=subtotal,
            taxable_amount=taxable_amount,
            total_amount=total_amount
        )

        invoice_id =  await self.repository.create(invoice_data)

        extensions = [".jpg", ".jpeg", ".png"]

        #Save delivery-proof photo
        file_name, file_path = await self.filehandler.save_file(photo , PRODUCT_PHOTO_FOLDER , extensions)

        #Save photo details in the database
        await self.repository.save_file_record(invoice_id,file_name,"product_photo",file_path)

        return {
            "message": "Invoice and product photo saved successfully",
            "invoice_id": invoice_id,
          "photo": file_name}
    

    async def get_invoices(self, limit, offset):
            return await self.repository.getall(limit, offset)

    async def get_invoice_by_id(self,invoice_id):
        result =  await self.repository.get_by_id(invoice_id)
        if result is None:
             raise InvoiceNotFoundError("invoice not found")
        return result

    async def update_invoice(self,invoice_id,invoice):

        subtotal = invoice.quantity * invoice.unit_price

        if subtotal < 10000:
            discount_percentage = 5
        elif subtotal <= 50000:
            discount_percentage = 10
        else:
            discount_percentage = 15

        discount_amount = subtotal * discount_percentage / 100

        taxable_amount = subtotal - discount_amount

        tax_percentage = 18

        tax_amount = taxable_amount * tax_percentage / 100

        total_amount = taxable_amount + tax_amount

        invoice_data = InvoiceData(
                    invoice_number=invoice.invoice_number,
                    customer_email=invoice.customer_email,
                    invoice_date=invoice.invoice_date,
                    customer_name=invoice.customer_name,
                    product_name=invoice.product_name,
                    quantity=invoice.quantity,
                    unit_price=invoice.unit_price,
                    discount_percentage=discount_percentage,
                    discount_amount=discount_amount,
                    tax_percentage=tax_percentage,
                    tax_amount=tax_amount,
                    subtotal=subtotal,
                    taxable_amount=taxable_amount,
                    total_amount=total_amount
                )
        
        result = await self.repository.update(invoice_id,invoice_data)


        if result is None:
            raise InvoiceNotFoundError("invoice not found")
        
        return result

    
    async def patch_invoice(self, invoice_id, invoice : InvoicePatch):

        existing_invoice = await self.repository.get_by_id(invoice_id)

        if existing_invoice is None:
            raise InvoiceNotFoundError("Invoice not found")

        updated_data = invoice.model_dump(exclude_unset=True)

        existing_invoice.update(updated_data)

        quantity = existing_invoice["quantity"]
        unit_price = existing_invoice["unit_price"]

        subtotal = quantity * unit_price

        if subtotal < 10000:
            discount_percentage = 5
        elif subtotal <= 50000:
            discount_percentage = 10
        else:
            discount_percentage = 15

        discount_amount = subtotal * discount_percentage / 100

        taxable_amount = subtotal - discount_amount

        tax_percentage = 18
        tax_amount = taxable_amount * tax_percentage / 100

        total_amount = taxable_amount + tax_amount

        invoice_data = InvoiceData(
            invoice_number=existing_invoice["invoice_number"],
            customer_name=existing_invoice["customer_name"],
            customer_email=existing_invoice["customer_email"],
            invoice_date=existing_invoice["invoice_date"],
            product_name=existing_invoice["product_name"],
            quantity=quantity,
            unit_price=unit_price,
            discount_percentage=discount_percentage,
            discount_amount=discount_amount,
            tax_percentage=tax_percentage,
            tax_amount=tax_amount,
            subtotal=subtotal,
            taxable_amount=taxable_amount,
            total_amount=total_amount
        )

        return await self.repository.update(invoice_id, invoice_data)


    async def delete_invoice(self,invoice_id : int):

        result =  await self.repository.delete(invoice_id)

        if result is None:
            raise InvoiceNotFoundError("invoice not found")

        return result

    
    
    async def upload_delivery_proof(self, invoice_id: int, photo):

        existing_invoice = await self.repository.get_by_id(invoice_id)

        if not existing_invoice:
            raise InvoiceNotFoundError("Invoice not found")
        
        extensions = [".pdf"]
        #  Save the delivery-proof photo
        file_name, file_path = await self.filehandler.save_file(photo , DELIVERY_PROOF_FOLDER ,extensions)

        # Save the photo details in the database
        await self.repository.save_file_record(invoice_id, file_name,"delivery_proof",file_path)

        return {
            "message": "Delivery-proof photo saved successfully",
            "invoice_id": invoice_id,
            "photo": file_name
        }
