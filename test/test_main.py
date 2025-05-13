# Python
import unittest
from unittest.mock import patch, MagicMock
from src.main import main

class TestMain(unittest.TestCase):
    @patch("main.get_file_names")
    @patch("main.create_patient_table")
    @patch("main.get_file_data")
    @patch("main.insert_patient")
    @patch("main.insert_new_resource")
    def test_main_no_files(self, mock_insert_new_resource, mock_insert_patient, mock_get_file_data, mock_create_patient_table, mock_get_file_names):
        # Mock get_file_names to return an empty list
        mock_get_file_names.return_value = []

        # Mock cursor
        mock_cursor = MagicMock()

        # Assert exception is raised when no files are found
        with self.assertRaises(Exception) as context:
            main(mock_cursor)
        self.assertEqual(str(context.exception), "No files found in data directory")

    @patch("main.get_file_names")
    @patch("main.create_patient_table")
    @patch("main.get_file_data")
    @patch("main.insert_patient")
    @patch("main.insert_new_resource")
    def test_main_process_files(self, mock_insert_new_resource, mock_insert_patient, mock_get_file_data, mock_create_patient_table, mock_get_file_names):
        # Mock get_file_names to return a list of files
        mock_get_file_names.return_value = ["file1.json"]

        # Mock get_file_data to return valid data
        mock_get_file_data.return_value = {
            "entry": [
                {"resourceType": "Patient", "id": "123", "name": "John Doe"},
                {"resourceType": "Observation", "id": "456", "value": "Test"}
            ]
        }

        # Mock cursor
        mock_cursor = MagicMock()

        # Call main
        main(mock_cursor)

        # Assert create_patient_table was called
        mock_create_patient_table.assert_called_once_with(mock_cursor)

        # Assert insert_patient was called
        mock_insert_patient.assert_called_once_with(mock_cursor, {"resourceType": "Patient", "id": "123", "name": "John Doe"})

        # Assert insert_new_resource was called
        mock_insert_new_resource.assert_called_once_with(mock_cursor, {"resourceType": "Observation", "id": "456", "value": "Test"}, "123")

    @patch("main.get_file_names")
    @patch("main.create_patient_table")
    @patch("main.get_file_data")
    @patch("main.insert_patient")
    @patch("main.insert_new_resource")
    def test_main_file_processing_error(self, mock_insert_new_resource, mock_insert_patient, mock_get_file_data, mock_create_patient_table, mock_get_file_names):
        # Mock get_file_names to return a list of files
        mock_get_file_names.return_value = ["file1.json"]

        # Mock get_file_data to raise an exception
        mock_get_file_data.side_effect = Exception("File read error")

        # Mock cursor
        mock_cursor = MagicMock()

        # Call main
        main(mock_cursor)

        # Assert create_patient_table was called
        mock_create_patient_table.assert_called_once_with(mock_cursor)

        # Assert insert_patient and insert_new_resource were not called
        mock_insert_patient.assert_not_called()
        mock_insert_new_resource.assert_not_called()

if __name__ == "__main__":
    unittest.main()