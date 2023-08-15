def validate_serializer(serializer_attr_name: str):
    def executor_func(body_func):
        def validate(self):
            serializer = getattr(self, serializer_attr_name).serializer
            if serializer.is_valid(raise_exception=True):
                return body_func(self)
        return validate
    return executor_func
