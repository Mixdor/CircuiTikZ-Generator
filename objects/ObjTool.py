class ObjTool:

    def __init__(self, name, name_class, number_pins, image_path, latex):
        self.name = name
        self.name_class = name_class
        self.number_pins = number_pins
        self.image = image_path
        self.latex = latex

    def get_name(self):
        return self.name

    def set_name(self, new_name):
        self.name = new_name

    def get_name_class(self):
        return self.name

    def set_name_class(self, new_name):
        self.name = new_name

    def get_number_pins(self):
        return self.number_pins

    def set_number_pins(self, new_number_pins):
        self.number_pins = new_number_pins

    def get_image(self):
        return self.image

    def set_image(self, new_image_path):
        self.image = new_image_path

    def get_latex(self):
        return self.name

    def set_latex(self, new_latex):
        self.latex = new_latex
