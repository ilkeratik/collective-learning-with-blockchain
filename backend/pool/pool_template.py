class Pool:
    def __init__(self):
        self.pool_map = {}
    
    def add_to_pool(self, element):
        """
        Add an element to the pool map.
        """
        self.pool_map[element.id] = element
        
    def remove_from_pool_by_id(self, id):
        """
        Remove an element from the pool map by id.
        """
        if id in self.pool_map:
            del self.pool_map[id]
        else:
            raise('Given id is not in the pool')

    def is_exists_by_id(self, id):
        """
        Check if a id exists in the pool map
        and return the value if found.
        """
        if id in self.pool_map:
            return self.pool_map[id]
        raise('Given id is not in the pool')
    
    def pool_data(self):
        """
        Return the transactions of the transaction pool represented in their
        json serialized form.
        """
        return list(map(
            lambda element: element.to_dict(),
            self.pool_map.values()
        ))

    