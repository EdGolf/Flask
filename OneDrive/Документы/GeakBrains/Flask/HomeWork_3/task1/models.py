from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    students = db.relationship('Student', backref='faculty', lazy=True)

    def __repr__(self):
        return f"Faculty({self.name})"


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    group = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(80), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'), nullable=False)
    grades = db.relationship('Performance', backref='student', lazy=True)

    def __repr__(self):
        return f"Student({self.firstname}, {self.lastname})"


class Grade(db.Model):
    value = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String(20), nullable=False)
    grades = db.relationship('Performance', backref='grade', lazy=True)

    def __repr__(self):
        return f"Grade({self.alias})"


class Discipline(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    grades = db.relationship('Performance', backref='discipline', lazy=True)

    def __repr__(self):
        return f"Discipline({self.name})"


class Performance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    discipline_id = db.Column(db.Integer, db.ForeignKey('discipline.id'), nullable=False)
    grade_value = db.Column(db.Integer, db.ForeignKey('grade.value'), nullable=False)