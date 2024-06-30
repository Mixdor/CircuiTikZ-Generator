class ObjComponent:

    def __init__(self, num, name, group_name, class_name, seed_latex, middle_point, angle, positions, label, drawables, latex):
        self.num = num
        self.name = name
        self.group_name = group_name
        self.class_name = class_name
        self.seed_latex = seed_latex
        self.middle_point = middle_point
        self.angle = angle
        self.positions = positions
        self.label = label
        self.drawables = drawables
        self.latex = latex

    @property
    def num(self):
        return self._num

    @num.setter
    def num(self, new_num):
        self._num = new_num

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
        return self._pins

    @class_name.setter
    def class_name(self, new_pins):
        self._pins = new_pins

    @property
    def seed_latex(self):
        return self._seed_latex

    @seed_latex.setter
    def seed_latex(self, new_seed_latex):
        self._seed_latex = new_seed_latex

    @property
    def middle_point(self):
        return self._middle_point

    @middle_point.setter
    def middle_point(self, new_middle_point):
        self._middle_point = new_middle_point

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, new_angle):
        self._angle = new_angle

    @property
    def positions(self):
        return self._positions

    @positions.setter
    def positions(self, new_positions):
        self._positions = new_positions

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, new_label):
        self._label = new_label

    @property
    def drawables(self):
        return self._drawables

    @drawables.setter
    def drawables(self, new_drawables):
        self._drawables = new_drawables

    @property
    def latex(self):
        return self._latex

    @latex.setter
    def latex(self, new_latex):
        self._latex = new_latex
