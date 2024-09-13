
class BackApiUtils:
    @staticmethod
    def convert_response_to_model(response, model_class):
        return model_class.from_dict(response.json(), is_response=True)