def validate_serializer(serializer_attr_name: str):
    def executor_func(body_func):
        def start_func(self):
            serializer = getattr(self, serializer_attr_name).serializer
            if serializer.is_valid(raise_exception=True):
                return body_func(self)

        return start_func

    return executor_func
