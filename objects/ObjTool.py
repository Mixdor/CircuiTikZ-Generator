class ObjTool:

    def __init__(self, name, group_name, class_name, image, image_static, latex):
        self.name = name
        self.group_name = group_name
        self.class_name = class_name
        self.image = image
        self.image_static = image_static
        self.latex = latex

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @property
    def group_name(self):
        return self._group_name

    @group_name.setter
    def group_name(self, new_group_name):
        self._group_name = new_group_name

    @property
    def class_name(self):
        return self._name_class

    @class_name.setter
    def class_name(self, new_name_class):
        self._name_class = new_name_class

    @property
    def image(self):
        return self._image_path

    @image.setter
    def image(self, new_image_path):
        self._image_path = new_image_path

    @property
    def image_static(self):
        return self._image_static

    @image_static.setter
    def image_static(self, new_image_static):
        self._image_static = new_image_static

    @property
    def latex(self):
        return self._latex

    @latex.setter
    def latex(self, new_latex):
        self._latex = new_latex
