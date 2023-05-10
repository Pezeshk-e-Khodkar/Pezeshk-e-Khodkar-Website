from django.db import models
from django.contrib.auth.models import User
import ast


class Result(models.Model):
    """Result table of dataset
    params:
        - disease_type: Type of disease
        - signature: Signature of image
        - result: Results as a dictionary
        - user: user that uses that result
    """
    disease_type = models.CharField(max_length=64)
    signature = models.CharField(max_length=64)
    image_format = models.CharField(max_length=64)
    result = models.TextField()
    user = models.ManyToManyField(User)

    _melanoma_help_link = "https://pardiscancer.com/blog/%D9%85%D9%84%D8%A7%D9%86%D9%88%D9%85%D8%A7"
    _basal_cell_carcinomas_help_link = "https://doctoreto.com/blog/about-basal-cell-carcinoma/#:~:text=%DA%A9%D8%A7%D8%B1%D8%B3%DB%8C%D9%86%D9%88%D9%85%20%D8%A8%D8%A7%D8%B2%D8%A7%D9%84%20%D9%86%D9%88%D8%B9%DB%8C%20%D8%B3%D8%B1%D8%B7%D8%A7%D9%86%20%D8%A7%D8%B3%D8%AA,%D9%86%D9%88%D8%B9%20%D8%B3%D9%84%D9%88%D9%84%E2%80%8C%D9%87%D8%A7%DB%8C%20%D8%B3%D8%B1%D8%B7%D8%A7%D9%86%DB%8C%20%D8%A7%DB%8C%D8%AC%D8%A7%D8%AF%20%D9%85%DB%8C%E2%80%8C%D8%B4%D9%88%D9%86%D8%AF."
    _squamous_cell_carcinoma_help_link = "https://doctoreto.com/blog/about-squamous-cell-carcinoma/"

    def result_as_json(self):
        # Result as a dictionary
        return ast.literal_eval(self.result)

    def result_as_type(self):
        json_result = self.result_as_json()
        if self.disease_type == "SkinCancer":
            max_value = max(json_result["basal cell carcinomas"],
                            json_result["melanoma"],
                            json_result["squamous cell carcinoma"])
            if max_value <= 0.5:
                return "سالم"

            for disease in json_result:
                if json_result[disease] == max_value:
                    return self.type_as_persian(disease)
        else:
            raise ValueError("It doesn't have "+self.disease_type+".")

    def type_as_persian(self, disease):
        if disease == "basal cell carcinomas":
            return "کارسینوم سلول بازال"
        elif disease == "melanoma":
            return "ملانوما"
        elif disease == "squamous cell carcinoma":
            return "سرطان سلول سنگ‌فرشی"
        else:
            raise ValueError("It doesn't have "+disease+".")

    def disease_as_persian(self):
        if self.disease_type == "SkinCancer":
            return "تشخیص سرطان پوست"
        else:
            raise ValueError("It doesn't have "+self.disease_type+".")

    def result_help_link(self):
        result = self.result_as_type()
        if result == "ملانوما":
            return self._melanoma_help_link
        elif result == "کارسینوم سلول بازال":
            return self._basal_cell_carcinomas_help_link
        elif result == "سرطان سلول سنگ‌فرشی":
            return self._squamous_cell_carcinoma_help_link
