from django.core.exceptions import ValidationError
import string

def validate_length(value):
    if len(value) < 5:
        raise ValidationError("제목은 5자 이상 적어주세요!")


def validate_no_special_charactors(value):
    for char in value:
        if char in string.punctuation:
            raise ValidationError("특수문자는 포함할 수 없습니다.")
