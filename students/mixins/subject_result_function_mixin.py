
class SubjectResultFunctionMixin:
    def get_semester3_total(self):
        ''' 
            Get total grades for semester 3 subject
            return 2 grades values one for student and other
            one for the subject 
        '''
        s, t = self.total_subject_year_grades()
        total = self.exam_grade + t
        std_total = self.std_exam_grade + s
        return std_total, total

    def total_subject_grades(self):
        '''
            return text to show it in table
            for total subject grade include
            all semesters
        '''
        std_grades, grades = self.get_total()
        if self.semester.order == '3':
            std_grades, grades = self.get_semester3_total()
        return '{} / {} '.format(std_grades, grades)

    def total_subject_year_grades(self):
        ''' 
            get total subject year grades for semester 3
            return student and subject grades values
        '''

        std_total, total = self.std_year_works_grade, self.year_works_grade
        qs = self.__class__.objects.filter(
            subject=self.subject,
            semester__results_paper=self.semester.results_paper).exclude(id=self.id)
        if qs.exists():
            for obj in qs:
                s, t = obj.get_total()
                std_total += s
                total += t
        return std_total, total

    def get_total_subject_year_grades(self):

        ''' 
            return text to show it directly in table
            for total subject year grades
        '''
        s, t = self.total_subject_year_grades()
        return '{} / {}'.format(s, t)