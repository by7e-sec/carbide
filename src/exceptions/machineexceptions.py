class MachineNotFoundException(Exception):
    err: str = ""

    def __init__(self, machine_name: str) -> None:
        self.err = f"Missing machine {machine_name} in config!"

        super().__init__(self.err)
