class Marker:
    def __init__(self, name, path_string):
        self.name = name
        self.path_string = path_string
    
    def is_same_name_marker(self, marker: Marker):
        return self.name == marker.name