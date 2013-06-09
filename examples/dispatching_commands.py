from simplecqrs.inventory import *
from simplecqrs.persistence import *
from simplecqrs.commands_handler import *
from simplecqrs.fake_bus import *

class DummyPublisher(object):
    def publish(self, event):
        pass #no-op

event_store = InMemoryEventStore(DummyPublisher())
repository = Repository(InventoryItem, event_store)
commands_handler = InventoryCommandsHandler(repository)
bus = FakeBus()

# registering all available commands
for command in [CreateInventoryItem, RenameInventoryItem, DeactivateInventoryItem,
                CheckInItemsToInventory, RemoveItemsFromInventory]:
    bus.register_handler(command, commands_handler)

# sending some commands
bus.send(CreateInventoryItem(0, 'hammer'))
bus.send(CreateInventoryItem(1, 'nails'))
bus.send(RenameInventoryItem(1, 'nails 2.5cm', 0))
bus.send(CheckInItemsToInventory(0, 10, 0))
bus.send(CheckInItemsToInventory(1, 1000, 1))
bus.send(RemoveItemsFromInventory(0, 1, 1))
bus.send(RemoveItemsFromInventory(1, 100, 2))


# results
hammer = repository.find_by_id(0)
nails = repository.find_by_id(1)

print '# hammer: '
print hammer.name
print hammer.count

print '# nails: '
print nails.name
print nails.count
