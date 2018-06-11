from models.store import StoreModel
from models.item import ItemModel
from tests.base_test import BaseTest
import json



class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/store/Test store')

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name('Test store'))
                self.assertEqual({'id': 1, 'name': 'Test store', 'items': []}, json.loads(response.data))

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/Test store')
                response = client.post('/store/Test store')

                self.assertEqual(response.status_code, 400)
                self.assertEqual({'message': "A store with name 'Test store' already exists."}, json.loads(response.data))

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/Test store')
                response = client.delete('/store/Test store')

                self.assertEqual({'message': 'Store deleted'}, json.loads(response.data))

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/Test store')
                response = client.get('/store/Test store')

                self.assertEqual(response.status_code, 200)
                self.assertEqual({'id': 1, 'name': 'Test store', 'items': []}, json.loads(response.data))

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/store/Test store2')

                self.assertEqual(response.status_code, 404)
                self.assertEqual({'message': 'Store not found'}, json.loads(response.data))

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/Test store')
                response_item_creation = client.post('/item/Test item', data={'name': 'Test item', 'price': 19.95, 'store_id': 1})

                self.assertEqual(json.loads(response_item_creation.data), {'name': 'Test item', 'price': 19.95})

                response = client.get('/store/Test store')
                self.assertEqual(response.status_code, 200)
                self.assertEqual({'id': 1, 'name': 'Test store', 'items': [{'name': 'Test item', 'price': 19.95}]}, json.loads(response.data))

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/Test store')
                client.post('/store/Test store 2')
                response = client.get('/stores')

                self.assertEqual({'stores': [{'id': 1, 'name': 'Test store', 'items': []},
                                             {'id': 2, 'name': 'Test store 2', 'items': []}]},
                                 json.loads(response.data))

    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/Test store')
                client.post('/item/Test item', data={'name': 'Test item', 'price': 19.95, 'store_id': 1})
                client.post('/item/Test item 2', data={'name': 'Test item 2', 'price': 29.95, 'store_id': 1})
                response = client.get('/stores')

                self.assertEqual({'stores': [{'id': 1, 'name': 'Test store',
                                             'items': [{'name': 'Test item', 'price': 19.95},
                                                        {'name': 'Test item 2', 'price': 29.95}]}]},
                                 json.loads(response.data))