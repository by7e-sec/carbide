class MachineNotFoundException(Exception):
    message: str = ""

    def __init__(self, machine_name):
        self.message = f"Missing machine {machine_name} in config!"

        super.__init__(self.message)
