from django.core.exceptions import ValidationError
import string


def validate_length(value):
    if len(value) < 5:
        raise ValidationError("제목은 5자 이상 적어주세요!")


def validate_no_special_charactors(value):
    for char in value:
        if char in string.punctuation:
            raise ValidationError("특수문자는 포함할 수 없습니다.")


def contains_uppercase_letter(value):
    for char in value:
        if char.isupper():
            return True
    return False


def contains_lowercase_letter(value):
    for char in value:
        if char.islower():
            return True
    return False


def contains_number(value):
    for char in value:
        if char.isdigit():
            return True
    return False


# get_help_text를 위해 클래스로 생성
class CustomPasswordValidator:
    def validate(self, password, user=None):
        if (
                len(password) < 8 or
                not contains_uppercase_letter(password) or
                not contains_lowercase_letter(password) or
                not contains_number(password) 
        ):
            raise ValidationError("8자 이상이며 영문 대/소문자, 숫자를 포함해야 합니다.")

    # 어드민 페이지에서 비밀번호를 변경할 때 출력되는 내용
    def get_help_text(self):
        return "8자 이상이며 영문 대/소문자, 숫자를 포함해야 합니다."
