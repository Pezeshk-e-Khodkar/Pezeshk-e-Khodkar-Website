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

    def result_as_json(self):
        # Result as a dictionary
        return ast.literal_eval(self.result)

    def result_as_type(self):
        json_result = self.result_as_json()
        if self.disease_type == "SkinCancer":
            max_value = max(json_result["basal cell carcinomas"],
                            json_result["melanoma"],
                            json_result["squamous cell carcinoma"])
            if max_value <= 0.3:
                return "سالم"

            for disease in json_result:
                if json_result[disease] == max_value:
                    return self.type_as_persian(disease)
        else:
            raise ValueError("It doesnt have "+self.disease_type+".")

    def type_as_persian(self, disease):
        if disease == "basal cell carcinomas":
            return "کارسینوم سلول های بازال"
        elif disease == "melanoma":
            return "ملانوما"
        elif disease == "squamous cell carcinoma":
            return "سرطان سلول سنگ‌فرشی"
        else:
            raise ValueError("It doesnt have "+disease+".")
