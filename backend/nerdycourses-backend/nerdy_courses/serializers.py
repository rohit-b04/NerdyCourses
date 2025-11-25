from rest_framework import serializers


class UserSerializers(serializers.Serializer):
    def login(self, data):
        self.email = data.email
        self.password = data.password
        pass
    pass