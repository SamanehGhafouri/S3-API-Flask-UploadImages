import unittest
import mock
from app import upload


class TestAppUploadFunction(unittest.TestCase):

    def test_empty_filename(self):

        mock_file_object = mock.MagicMock()
        mock_file_object.filename = ''

        mock_flask_request = mock.MagicMock()
        mock_flask_request.files = {'file': mock_file_object}

        expected_response = {'ERROR': "No file name was provided!"}, 400
        with mock.patch('app.request', mock_flask_request):
            # call upload function from app.py
            actual_response = upload()

        self.assertEqual(expected_response, actual_response)

    def test_file_extension(self):

        mock_file_object = mock.MagicMock()
        mock_file_object.filename = 'file.pdf'

        mock_flask_request = mock.MagicMock()
        mock_flask_request.files = {'file': mock_file_object}

        expected_response = {'ERROR': "Accepting file types: .png, .jpg, .jpeg, .gif"}, 400
        with mock.patch('app.request', mock_flask_request):
            actual_response = upload()

        self.assertEqual(expected_response, actual_response)


if __name__ == '__main__':
    unittest.main()
