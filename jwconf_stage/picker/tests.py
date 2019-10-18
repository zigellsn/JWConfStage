from django.test import TestCase
from django.urls import reverse
import importlib

picker = importlib.import_module('picker.models')


def create_credential(congregation, autologin, username, password, extractor_url, touch):
    return picker.Credential.objects.create(congregation=congregation, autologin=autologin,
                                            username=username, password=password, extractor_url=extractor_url,
                                            touch=touch)


class PickerViewTests(TestCase):
    def test_no_congregation(self):
        response = self.client.get(reverse('picker:picker'))
        self.assertEquals(response.status_code, 200)

    def test_one_congregation(self):
        create_credential('LE', 'abc', 'abc', 'abc', 'www.abc.com', False)
        response = self.client.get(reverse('picker:picker'))
        self.assertEquals(response.status_code, 302)

    def test_many_congregations(self):
        credential_le = create_credential('LE', 'abc', 'abc', 'abc', 'www.abc.com', False)
        credential_fe = create_credential('FE', 'abc', 'abc', 'abc', 'www.abc.com', False)
        response = self.client.get(reverse('picker:picker'))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, credential_le)
        self.assertContains(response, credential_fe)
