class ResultPaperFunctionMixin:
    
    def get_part2_grades(self):
        '''  
            This function to get all second attempt compensatoires 
            exams grades related to this result paper
        '''
        return self.all_com_grades.filter(part='2')

    def get_part3_grades(self):
        '''  
            This function to get all third attempt compensatoires 
            exams grades related to this result paper
        '''
        return self.all_com_grades.filter(part='3')

    def current_final_semester(self):
        '''
            Get last active semester
        '''
        qs = self.semesters.active().values_list('order')
        semesters = [x[0] for x in qs]
        if '2' in semesters and '3' not in semesters:
            return '2'
        elif '3' in semesters:
            return '3'
        return '1'

    def current_part(self):
        '''
            Get last active attempt
        '''
        if self.part2 and not self.part3:
            return '2'
        elif self.part3:
            return '3'
        return None

    def passed_all(self):
        '''
            Check what if all semester subjects has been passed
        '''
        
        # lis = [x.passed_all() for x in self.semesters.active().filter(
        #     order=self.current_final_semester())]
        # return all(lis)

        passed = self.semesters.active().filter(
             order=self.current_final_semester()).first().passed_after_fail()
        return passed


    def total_grades(self):
        
        ''' this func to get total grades '''
        total, std_total = 0, 0
        qs = self.semesters.active()

        for semester in qs:
            t, s = semester.get_total_grades()
            total += t
            std_total += s
        
        return total, std_total

    def total_none_passed_exams(self):

        ''' this func to get the semester subjects results
             exams grades that not passed yet '''

        order = self.current_final_semester()
        
        total = 0
        semester = self.semesters.filter(order=order).first()
        if semester:
            total = semester.total_none_passed_exams()
        
        # total = 0
        # if int(order) > 1:
        #     qs = self.semesters.filter(order=order)
        #     total = sum([x.none_passed_exams_grade() for x in qs])
        
        return total

    def total_comps_grades(self, part=''):
        '''
          this func to get total grades for
           just one attempt results
        '''
        qs = self.all_com_grades.filter(
            part=part).values_list('std_exam_grade')
        return self.get_total_by_qs(qs)

    def get_total_grades(self):
        ''' this func to manage how to get total grades
             whether if part2 or part3 are active '''

        total, std_total = self.total_grades()
        if self.part2 and not self.part3:
            std_total = std_total - self.total_none_passed_exams() + \
                self.total_comps_grades(
                part='2')
        elif self.part3:
            std_total = std_total - self.total_none_passed_exams() + \
                self.total_comps_grades(
                part='3')
        return total, std_total
