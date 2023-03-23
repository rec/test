class LampDesc:
    instrument = None
    offset = 0

    def slice(self):
        return slice(self.offset, self.offset + bool(self.instrument))


print(LampDesc().slice())
