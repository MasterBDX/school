class SemesterFunctionMixin:
    def passed_all(self):
        passed = 0
        qs = self.subjects_results.values_list('passed', 'subject')
        for x in qs:
            if x[0] == True:
                passed += 1
        return passed == qs.count()
    
    def passed_after_fail(self):
        passed = 0
        qs = self.subjects_results.values_list('passed', 'subject')
        for x in qs:
            if x[0] == True:
                passed += 1
            else:
                part = self.results_paper.current_part()
                if part:
                    comp = self.results_paper.all_com_grades.filter(semester=self.order,
                                                                    subject=x[1],
                                                                    results_paper=self.results_paper,
                                                                    part=part).first()
                    if comp :
                        if comp.passed:
                            passed += 1
        return passed == qs.count()

    def get_total_grades(self):
        qs = self.subjects_results.values_list('exam_grade',
                                               'year_works_grade')
        qs2 = self.subjects_results.values_list('std_exam_grade',
                                                'std_year_works_grade')
        total = sum([sum(x) for x in qs])
        std_total = sum([sum(x) for x in qs2])
        return total, std_total


    def total_comps_grades(self, part='2'):
        '''
          this func to get total grades for
           just one attempt results
        '''
        qs = self.results_paper.all_com_grades.filter(
            part=part,
            semester=self.order).values_list('std_exam_grade')
        return self.get_total_by_qs(qs)
    
    def total_none_passed_exams(self):  
        ''' 
            this func to get the semester subjects results
            grades that not passed 
        '''

        qs = self.subjects_results.filter(
            passed=False).values_list('std_exam_grade')
        total = self.get_total_by_qs(qs)
        return total

    def total_after_fail(self):
        ''' 
            this func to manage how to get total grades
             whether if part2 or part3 are active 
        '''

        total, std_total = self.get_total_grades()
        if self.results_paper.part2 and not self.results_paper.part3:
            std_total = std_total - self.total_none_passed_exams() + \
                self.total_comps_grades(
                part='2')
        elif self.results_paper.part3:
            std_total = std_total - self.total_none_passed_exams() + \
                self.results_paper.total_comps_grades(
                part='3')
        return total, std_total

    def total_percentage_after_fail(self):
        total, std_total = self.total_after_fail()
        try:
            return round(std_total / total * 100, 1)
        except:
            return 0

    def general_average_after_fail(self):
        std_total, total = self.total_after_fail()
        return '{} \ {}'.format(total, std_total)
