class Lightbulb:
    def __init__(self):
        self.state = "off"

    # create method change_state here
    def change_state(self):
        if self.state == "on":
            print("Turning the light off")
            self.state = "off"
        else:
            print("Turning the light on")
            self.state = "on"
