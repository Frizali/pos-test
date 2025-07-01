from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def dashboard_page(self):
        self.client.get("/")

    @task
    def productList_page(self):
        self.client.get("/Product/ProductList?category=All")
