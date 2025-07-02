from locust import HttpUser, task, between
import uuid
import random
import string

class InventoryTestUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def inventoryList_page(self):
        self.client.get("/Inventory/Index?search=&searchPartType=")

    def generate_code(self, base, length):
        suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        return f"{base[:3].upper()}-{suffix}"

    @task(1)
    def add_inventory_part(self):
        payload = {
            "Part.PartId": str(uuid.uuid4()),
            "Part.PartTypeId": "5dd4b2f1-7a82-4b03-897f-aab1ef608b1d",
            "Part.UnitId": "804c73ad-2a57-45ee-b2b7-299a3d8c538d",
            "Part.PartName": "Tepung Terigu",
            "Part.PartCd": self.generate_code("Tepung Terigu", 6),
            "Part.PartQty": 5,
            "Part.Price": 50000,
            "Part.Note": "Periksa kondisi kemasan dan simpan di tempat yang kering dan tertutup rapat."
        }

        with self.client.post("/Inventory/AddInventory", data=payload, catch_response=True) as response:
            if response.status_code not in [200, 302]:
                response.failure(f"Gagal menambah part: {response.status_code}")

    @task(1)
    def delete_part(self):
        part_id = "c5b1eb0c-bd5e-4672-98be-8ef34db7f40a"
        with self.client.post(f"/Inventory/DeletePartConfirmed/{part_id}", catch_response=True) as response:
            if response.status_code not in [200, 302]:
                response.failure(f"Failed to delete part: {response.status_code}")