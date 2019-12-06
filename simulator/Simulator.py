
class Simulator(object):
    def __init__(self, func, image):
        self.func = func
        self.image = image

    def process(self):
        try:
            return self.func(self.image)
        except Exception as e:
            print("failed to simulate %s:\n%s" % (self.func, e))
            return None
