from locust import HttpUser, task, between
import uuid
import random
import os

class ProductTestUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        # Pastikan gambar tersedia di folder yang sama dengan locustfile
        self.image_path = r"C:\Users\acer\Pictures\Menu\mie-goreng.jpeg"
        if not os.path.exists(self.image_path):
            raise FileNotFoundError("File gambar tidak ditemukan.")

    @task
    def add_product_without_variant(self):
        product_id = str(uuid.uuid4())

        # Data form field
        form_data = {
            "Product.ProductId": product_id,
            "Product.ProductName": "Mie Goreng",
            "Product.ProductDescription": "Mie Goreng Spesial dengan bumbu rahasia",
            "Product.ProductCode": "MG01",
            "Product.CategoryId": "2A8E5E63-B80E-4991-86A5-AC05F00EDA23",
            "Product.Price": "15000",
            "Product.ProductStock": "1000"
        }

        # Gambar (mimic IFormFile)
        with open(self.image_path, "rb") as img:
            files = {
                "productImage": (os.path.basename(self.image_path), img, "image/png")
            }

            with self.client.post(
                "/Product/Save",
                data=form_data,
                files=files,
                catch_response=True
            ) as response:
                if response.status_code not in [200, 201, 302]:
                    response.failure(f"Gagal tambah produk: {response.status_code}")
                else:
                    response.success()
