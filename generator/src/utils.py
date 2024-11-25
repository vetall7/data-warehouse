import os
import random
import pandas as pd


class Range:
    def __init__(self, min, max):
        self.min = min
        self.max = max

    def random(self):
        return random.randint(self.min, self.max)
    

class Attendance:
    def __init__(self, student_pesel, present, excused):
        self.student_pesel = student_pesel
        self.present = present
        self.excused = excused


def save_to_csv(data, path, file_name):
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data', path)
    os.makedirs(data_dir, exist_ok=True)

    data_df = pd.DataFrame([vars(o) for o in data])
    save_path = os.path.join(data_dir, f'{file_name}.csv')

    data_df.to_csv(save_path, index=False)


def save_attendance_to_csv(attendance_data, data, path, file_name):
    """
    data.keys() = [(group_id, subject_id), ...]
    data[(group_id, subject_id)] = { date1: [Attendance, ...], date2: [Attendance, ...], ... }

    for each (group_id, subject_id) in data.keys():
        create separate CSV file
        CSV line 0: subject_name subject_year
        CSV line 1: group_grade group_name
        CSV line 2: ,,date1,,date2,,date3...
        CSV line 3: student2_name, student2_pesel, present, excused, present, excused, present, excused...
        CSV line 4: student2_name, student2_pesel, present, excused, present, excused, present, excused...
    """
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data', path, 'attendance')
    os.makedirs(data_dir, exist_ok=True)

    for (group_id, subject_id), attendance in attendance_data.items():
        save_path = os.path.join(data_dir, f'{file_name}_{group_id}_{subject_id}.csv')
        with open(save_path, 'w', encoding='utf-8') as f:
            subject = [subject for subject in data['subjects'] if subject.id == subject_id][0]
            group = [group for group in data['groups'] if group.id == group_id][0]
            f.write(f'{subject.name} {subject.year}\n')
            f.write(f'{group.grade} {group.name}\n')

            dates = sorted(attendance.keys())
            f.write(f',,{",".join([str(date) + "," for date in dates])}\n')

            student_pesels = list(map(lambda att: att.student_pesel, attendance[dates[0]]))

            for student_idx, student_pesel in enumerate(student_pesels):
                student = [student for student in data['students'] if student.pesel == student_pesel][0]
                f.write(f'{student.name},')
                f.write(f'{student.pesel},')

                for date in dates:
                    student_attendance = attendance[date][student_idx]
                    f.write(f'{student_attendance.present},{student_attendance.excused},')
                f.write('\n')

            f.write(',,')
            for date in dates:
                f.write(f'{_get_average_attendance(attendance[date])},,')
            f.write('\n')

def _get_average_attendance(attendances):
    return round(100 * sum([att.present for att in attendances]) / len(attendances), 2)
