class Setter:
    other_file = ''

    @property
    def project_file(self):
        return self._project_file

    @project_file.setter
    def project_file(self, project_file):
        self._project_file = project_file
