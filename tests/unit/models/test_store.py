from models.store import StoreModel
from tests.unit.unit_base_test import UnitBaseTest


class StoreTest(UnitBaseTest):
    def test_create_store(self):
        store = StoreModel('Test store')

        self.assertEqual(store.name, 'Test store',
                         "The name of the store after creation does not equal the constructor argument.")