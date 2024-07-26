class Vendor:
    def __init__(self, name, address, category, services):
        self.name = name
        self.category = category
        self.services = services
        self.address = address

    def serialize(self):
        return {
            'name': self.name,
            'category': self.category,
            'services': self.services,
            'address' : self.address
        }
