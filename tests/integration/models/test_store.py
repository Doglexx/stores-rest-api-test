from models.item import ItemModel
from models.store import StoreModel

from tests.base_test import BaseTest


class StoreTest(BaseTest):
    def test_create_store_items_empty(self):
        store = StoreModel('Test store')

        self.assertListEqual(store.items.all(), [], "The store's items list is not empty.")

    def test_crud(self):
        with self.app_context():
            store = StoreModel('Test store')

            self.assertIsNone(StoreModel.find_by_name('Test store'))

            store.save_to_db()

            self.assertIsNotNone(StoreModel.find_by_name('Test store'))

            store.delete_from_db()

            self.assertIsNone(StoreModel.find_by_name('Test store'))

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel('Test store')
            item = ItemModel('test_item', 19.99, 1)

            store.save_to_db()
            item.save_to_db()

            self.assertEqual(store.items.count(), 1)
            self.assertEqual(store.items.first().name, 'test_item')

    def test_store_json_with_item(self):
        with self.app_context():
            store = StoreModel('Test store')
            item = ItemModel('test_item', 19.99, 1)

            store.save_to_db()
            item.save_to_db()

            expected = {
                'name': 'Test store',
                'items': [{'name': 'test_item', 'price': 19.99}]
            }

            self.assertDictEqual(store.json(), expected)
