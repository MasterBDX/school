class CompensatoryExamsFunctionsMixin:
    def total_subject_grades(self):
        std_grades, grades = self.get_total()
        return '{} / {} '.format(std_grades, grades)