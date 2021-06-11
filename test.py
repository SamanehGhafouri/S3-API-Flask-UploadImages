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

    def test_uploaded_to_s3_successful(self):
        # mock filename
        mock_file_object = mock.MagicMock()
        mock_file_object.filename = 'file.png'

        # mock flask request uploaded_file = request.files['file']
        mock_flask_request = mock.MagicMock()
        mock_flask_request.files = {'file': mock_file_object}

        # mock generated_filename, generated_filename
        mock_generated_filename = mock.MagicMock(return_value='1234.png')

        # mock upload file obj
        mock_upload_file_obj = mock.MagicMock()

        expected_response = ({'generated_filename': '1234.png', 'original_filename': 'file.png', 'url': 'uploads/1234.png'}, 200)

        with mock.patch('app.request', mock_flask_request):
            with mock.patch('app.create_random_id', mock_generated_filename):
                with mock.patch('app.upload_file_obj', mock_upload_file_obj):
                    actual_response = upload()
        self.assertEqual(expected_response, actual_response)

    def test_uploaded_to_s3_not_successful(self):
        # mock filename
        mock_file_object = mock.MagicMock()
        mock_file_object.filename = 'file.png'

        # mock flask request uploaded_file = request.files['file']
        mock_flask_request = mock.MagicMock()
        mock_flask_request.files = {'file': mock_file_object}

        # mock generated_filename, generated_filename
        mock_generated_filename = mock.MagicMock(return_value='1234.png')

        # mock upload file obj throw an exception
        mock_upload_file_obj = mock.MagicMock(side_effect=Exception('mock exception'))

        expected_response = ({'ERROR': 'mock exception'}, 400)

        with mock.patch('app.request', mock_flask_request):
            with mock.patch('app.create_random_id', mock_generated_filename):
                with mock.patch('app.upload_file_obj', mock_upload_file_obj):
                    actual_response = upload()
        self.assertEqual(expected_response, actual_response)


if __name__ == '__main__':
    unittest.main()
