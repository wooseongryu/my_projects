from django.core.exceptions import ValidationError

def validate_length(value):
    if len(value) < 5:
        raise ValidationError("제목은 5자 이상 적어주세요!")
