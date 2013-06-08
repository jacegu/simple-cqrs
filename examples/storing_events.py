from simplecqrs.inventory import *
from simplecqrs.persistence import *

class DummyPublisher(object):
    def publish(self, event):
        pass #no-op

event_store = InMemoryEventStore(DummyPublisher())
repository  = Repository(InventoryItem, event_store)

inventory_item = InventoryItem(0, 'Nails')
inventory_item.rename('2.5cm nails')
inventory_item.check_in(1000)
inventory_item.remove(100)
inventory_item.deactivate()

print '# before saving'
print inventory_item.name
print inventory_item.count
print 'Active' if inventory_item.is_active else 'Inactive'

repository.save(inventory_item)

print
print '> Event Store state'
print event_store.events
print

inventory_item = repository.find_by_id(inventory_item.id)

print '# after recovering from the repository'
print inventory_item.name
print inventory_item.count
print 'Active' if inventory_item.is_active else 'Inactive'
