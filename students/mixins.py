class SubjectsResultsMixin:
    def need_to_pass_exam(self):
        result = "0"
        grade = self.exam_pass_grade - self.std_exam_grade
        try:
            percentage = grade / self.exam_grade * 100
            if grade > 0:
                result = '{} ({}%)'.format(grade, round(percentage, 1))
        except:
            pass
        return result

    def get_total(self):
        total = self.exam_grade + self.year_works_grade
        std_total = self.std_exam_grade + self.std_year_works_grade
        return std_total, total

    def get_total(self):
        total = self.exam_grade + self.year_works_grade
        std_total = self.std_exam_grade + self.std_year_works_grade
        return std_total, total


class FinalResultsMixin:
    def total_percentage(self):
        total, std_total = self.get_total_grades()
        try:
            return round(std_total / total * 100, 1)
        except:
            return 0

    def general_average(self):
        std_total, total = self.get_total_grades()

        return '{} \ {}'.format(total, std_total)

    def get_estimate(self):
        if self.passed_all():
            if self.total_percentage() <= 100 and self.total_percentage() > 84:
                return 'ممتاز'
            elif self.total_percentage() <= 84 and self.total_percentage() > 74:
                return 'جيد جدا'
            elif self.total_percentage() <= 74 and self.total_percentage() > 64:
                return 'جيد'
            elif self.total_percentage() <= 64 and self.total_percentage() > 54:
                return 'مقبول'
            elif self.total_percentage() <= 54 and self.total_percentage() > 30:
                return 'ضعيف'
            elif self.total_percentage() <= 30 and self.total_percentage() >= 0:
                return 'ضعيف جدا'
            else:
                return ' '
        return 'راسب'

    def get_total_by_qs(self, qs):
        if qs.exists():
            total = sum([x[0] for x in qs])
            return total
        return 0
