from locust import HttpUser, task, between
import uuid
import random

class OrderFlowTestUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def full_order_flow(self):
        order_id = str(uuid.uuid4())
        total_amount = (3 * 2000) + (5 * 7000)

        order_items = [
            {
                "ProductId": "bfd581c3-f2ba-44f8-8e8c-2b314305a056",
                "Quantity": 3,
                "UnitPrice": 2000,
                "SubTotal": 3 * 2000,
                "Notes": "-"
            },
            {
                "ProductId": "c41f2f36-9d8b-430d-8c3c-f20a4d448f0b",
                "Quantity": 5,
                "UnitPrice": 7000,
                "SubTotal": 5 * 7000,
                "Notes": "-"
            }
        ]

        snap_payload = {
            "orderId": order_id,
            "totalAmount": total_amount,
            "TblOrderItems": order_items,
            "type": "Regular",
            "scheduledAt": None,
            "notes": "Test order"
        }

        # Step 1: POST ke GetSnapToken
        with self.client.post(
            "/Order/GetSnapToken",
            json=snap_payload,
            catch_response=True
        ) as snap_response:

            if snap_response.status_code != 200:
                snap_response.failure(f"SnapToken gagal: {snap_response.status_code}")
                return

            # Step 2: GET ke CreateOrder (pakai session cookie yang sama)
            with self.client.get(
                f"/Order/CreateOrder?orderId={order_id}&isTest=True",
                catch_response=True
            ) as create_response:
                if create_response.status_code != 200:
                    create_response.failure(f"CreateOrder gagal: {create_response.status_code}")
                else:
                    create_response.success()