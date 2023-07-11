from flask import FlaskForm


class RegisterForm(FlaskForm):
    nickname = StringField('Ник', validators=[DataRequired()])
    firstname = StringField('Имя', validators=[DataRequired()])
    lastname = StringField('Фамилия', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email("Не корректный e-mail")])
    birth_date = DateField('Дата рождения',  format='%Y-%m-%d')
    password = PasswordField("Пароль: ", validators=[DataRequired()])
    confirm_psw = PasswordField("Подтверждение пароля: ",
                                validators=[DataRequired(), EqualTo('password', message="Пароли не совпадают")])
    сonsent = BooleanField("Даю согласие на обработку персональных данных", validators=[DataRequired(), ])
    submit = SubmitField("Регистрация")

    def validate_password(form, field):
        if len(field.data) < 8:
            raise ValidationError('Длина должна быть не менее 8 символов')
        if not any(map(str.isdigit, field.data)):
            raise ValidationError('Пароль должен содержать хотя бы одну цифру')
        if not any(map(str.isalpha, field.data)):
            raise ValidationError('Пароль должен содержать хотя бы одну букву')

    def validate_nickname(form, field):
        user = User.query.filter_by(nickname=field.data).first()
        if user is not None:
            raise ValidationError('Пользователь с таким ником уже зарегистрирован')

    def validate_email(form, field):
        user = User.query.filter_by(email=field.data).first()
        if user is not None:
            raise ValidationError('Пользователь с таким email уже зарегистрирован')