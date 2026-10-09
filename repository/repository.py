from schemas.schemas import InvoiceCreate
from database.database import get_connection


class Repository:

    async def create(self,invoice):
        connection = await get_connection()

        try:
            async with connection.cursor() as cursor:

                await cursor.execute(
                    """INSERT INTO invoices(
                    invoice_number,
                    customer_name,
                    customer_email,
                    invoice_date,
                    product_name,
                    quantity,
                    unit_price,
                    discount_percentage,
                    discount_amount,
                    tax_percentage,
                    tax_amount,
                    subtotal,
                    taxable_amount,
                    total_amount
                    )
                    VALUES( %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s)
                    RETURNING id""",
                    (
                    invoice.invoice_number,
                    invoice.customer_name,
                    invoice.customer_email,
                    invoice.invoice_date,
                    invoice.product_name,
                    invoice.quantity,
                    invoice.unit_price,
                    invoice.discount_percentage,
                    invoice.discount_amount,
                    invoice.tax_percentage,
                    invoice.tax_amount,
                    invoice.subtotal,
                    invoice.taxable_amount,
                    invoice.total_amount)
                )

                result = await cursor.fetchone()

                invoice_id = result[0]
                await connection.commit()

                return invoice_id
            


        finally:
            await connection.close()

    async def getall(self , limit: int, offset: int):
        connection = await get_connection()

        try:

           async with connection.cursor() as cursor:
                await cursor.execute("""SELECT
                    invoice_number,
                    customer_email ,
                    invoice_date,
                    customer_name,
                    product_name ,
                    quantity ,
                    unit_price,
                    discount_percentage ,
                    discount_amount ,
                    tax_percentage ,
                    tax_amount ,
                    subtotal ,
                    taxable_amount
                    total_amount
                    FROM invoices 
                    ORDER BY id 
                    LIMIT %s
                    offset %s""",
                    (limit,offset))
                
                results = await cursor.fetchall()
                columns = [value[0] for value in cursor.description]

                return [dict(zip(columns,result)) for result in results]
                
            
        finally:
            await connection.close()


    async def get_by_invoice_number(self,invoice_id : str):

        connection = await get_connection()
        try:
            async with connection.cursor() as cursor:
                await cursor.execute("""
                               select
                                invoice_number,
                                customer_email ,
                                invoice_date,
                                customer_name,
                                product_name ,
                                quantity ,
                                unit_price,
                                discount_percentage ,
                                discount_amount ,
                                tax_percentage ,
                                tax_amount ,
                                subtotal ,
                                taxable_amount
                                total_amount
                                from invoices WHERE invoice_number = %s
                                """,(invoice_id,))
                return  await cursor.fetchone()   
        finally:
            await connection.close()


    async def get_by_id(self, invoice_id):

        connection = await get_connection()

        try:
           async with connection.cursor() as cursor:

                await cursor.execute(
                    """select
                                 invoice_number,
                                 customer_email ,
                                 invoice_date,
                                 customer_name,
                                 product_name ,
                                 quantity ,
                                 unit_price,
                                 discount_percentage ,
                                 discount_amount ,
                                 tax_percentage ,
                                 tax_amount ,
                                 subtotal ,
                                 taxable_amount
                                 total_amount
                                 from invoices WHERE id = %s
                                """,
                    (invoice_id,)
                )

                invoice = await cursor.fetchone()


                if invoice is None:
                    return None

                columns = [description[0] for description in cursor.description]

                return dict(zip(columns, invoice))

        finally:
            await connection.close()

    async def update(self,invoice_id : int,invoice):
        connection = await get_connection()
        try:
            async with connection.cursor() as cursor:
                await cursor.execute("""
                                UPDATE invoices SET
                                invoice_number = %s,
                                customer_name = %s,
                                customer_email = %s ,
                                invoice_date = %s,
                                product_name = %s ,
                                quantity = %s ,
                                unit_price = %s,
                                discount_percentage = %s ,
                                discount_amount = %s ,
                                tax_percentage = %s ,
                                tax_amount = %s ,
                                subtotal = %s ,
                                taxable_amount = %s,
                                total_amount = %s WHERE id = %s
                                """,( invoice.invoice_number,
                                    invoice.customer_name,
                                    invoice.customer_email,
                                    invoice.invoice_date,
                                    invoice.product_name,
                                    invoice.quantity,
                                    invoice.unit_price,
                                    invoice.discount_percentage,
                                    invoice.discount_amount,
                                    invoice.tax_percentage,
                                    invoice.tax_amount,
                                    invoice.subtotal,
                                    invoice.taxable_amount,
                                    invoice.total_amount,
                                    invoice_id))

                if cursor.rowcount == 0 :
                    return None
                
                await connection.commit()

                return {"msg" : f"invoice : {invoice_id} updated"}
            
        finally:
            await connection.close()


    async def delete(self , invoice_id : int):
        connection = await get_connection()
        try:

            async with connection.cursor() as cursor:
                await cursor.execute("""
                                DELETE FROM invoices WHERE id = %s
                                """,(invoice_id,))

                if cursor.rowcount == 0:
                    return None
                
                await connection.commit()

                return {"msg" : f"deleted the row id {invoice_id}"}
            
        finally:
            await connection.close()
    
    async def save_file_record(self,invoice_id: int,file_name: str,file_type: str,file_path: str):
        connection = await get_connection()

        try:
            async with connection.cursor() as cursor:
                await cursor.execute(
                    """
                    INSERT INTO invoice_files
                    (invoice_id, file_name, file_type, file_path)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (invoice_id, file_name, file_type, file_path)
                )

            await connection.commit()

        finally:
            await connection.close()