from threa import IsThread


class Thread(IsThread):
    def callback(self):
        raise ValueError('OOPS')


Thread().start()
