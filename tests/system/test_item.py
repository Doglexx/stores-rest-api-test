from models.store import StoreModel
from models.user import UserModel
from models.item import ItemModel
from tests.base_test import BaseTest
import json


class ItemTest(BaseTest):
    def setUp(self):
        super(ItemTest, self).setUp()  # BaseTest.setUp(self)

        with self.app() as client:
            with self.app_context():
                UserModel('Test user', '1234').save_to_db()

                client_auth_response = client.post('/auth', data=json.dumps({'username': 'Test user', 'password': '1234'}),
                                    headers={'Content-Type': 'application/json'})
                self.access_token = 'JWT ' + json.loads(client_auth_response.data)['access_token']

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/item/Test item')

                self.assertEqual(401, response.status_code)
                self.assertEqual(json.loads(response.data)['message'], 'Could not authorize. Did you include a valid Authorization header?')

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/item/Test item', headers={'Authorization': self.access_token})

                self.assertEqual(404, response.status_code)
                self.assertEqual('Item not found', json.loads(response.data)['message'])


    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('Test store').save_to_db()
                ItemModel('Test item', 19.95, 1).save_to_db()
                response = client.get('/item/Test item', headers={'Authorization': self.access_token})

                self.assertEqual(200, response.status_code)
                self.assertEqual({'name': 'Test item', 'price': 19.95}, json.loads(response.data))


    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('Test store').save_to_db()
                ItemModel('Test item', 19.95, 1).save_to_db()

                response = client.delete('/item/Test item')
                self.assertEqual(200, response.status_code)
                self.assertEqual({'message': 'Item deleted'}, json.loads(response.data))


    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('Test store').save_to_db()

                response = client.post('/item/Test item', data={'price': 19.95, 'store_id': 1})

                self.assertEqual(201, response.status_code)
                self.assertEqual({'name': 'Test item', 'price': 19.95}, json.loads(response.data))

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('Test store').save_to_db()
                ItemModel('Test item', 19.95, 1).save_to_db()

                response = client.post('/item/Test item', data={'price': 19.95, 'store_id': 1})

                self.assertEqual(400, response.status_code)
                self.assertEqual({'message': "An item with name 'Test item' already exists."}, json.loads(response.data))


    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('Test store').save_to_db()

                response = client.put('/item/Test item', data={'price': 9.95, 'store_id': 1})

                self.assertEqual(200, response.status_code)
                self.assertEqual(9.95, ItemModel.find_by_name('Test item').price)
                self.assertEqual({'name': 'Test item', 'price': 9.95}, json.loads(response.data))


    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('Test store').save_to_db()
                ItemModel('Test item', 19.95, 1).save_to_db()

                self.assertEqual(19.95, ItemModel.find_by_name('Test item').price)

                response = client.put('/item/Test item', data={'name': 'New test item', 'price': 9.95, 'store_id': 1})

                self.assertEqual({'name': 'Test item', 'price': 9.95}, json.loads(response.data))

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('Test store').save_to_db()
                ItemModel('Test item', 19.95, 1).save_to_db()
                ItemModel('Test item 2', 29.95, 1).save_to_db()

                response = client.get('/items')

                self.assertEqual({'items': [{'name': 'Test item', 'price': 19.95}, {'name': 'Test item 2', 'price': 29.95}]},
                                 json.loads(response.data))
