import unittest
import tempfile
import shutil
from pathlib import Path
from unittest import mock
from unittest.mock import patch

from kernpy.__main__ import (
    handle_ekern2kern,
    handle_kern2ekern,
    handle_polish_exporter,
)


class MainTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)
        self.nested_dir = self.temp_path / "nested"
        self.nested_dir.mkdir()

    def tearDown(self):
        self.temp_dir.cleanup()

    def create_file(self, path: Path, content: str = "test"):
        path.write_text(content)
        return path

    @patch("kernpy.__main__.ekern_to_krn")
    def test_ekern2kern_single_file(self, mock_convert):
        file = self.create_file(self.temp_path / "file.ekrn")
        args = mock.Mock(input_path=str(file), output_path=None, recursive=False, verbose=1)

        handle_ekern2kern(args)

        mock_convert.assert_called_once_with(str(file), str(file.with_suffix(".krn")))

    @patch("kernpy.__main__.ekern_to_krn")
    def test_ekern2kern_recursive_multiple(self, mock_convert):
        f1 = self.create_file(self.nested_dir / "a.ekrn")
        f2 = self.create_file(self.nested_dir / "b.ekern")

        args = mock.Mock(input_path=str(self.temp_path), output_path=None, recursive=True, verbose=1)

        handle_ekern2kern(args)

        expected_calls = [
            mock.call(str(f1), str(f1.with_suffix(".krn"))),
            mock.call(str(f2), str(f2.with_suffix(".krn")))
        ]
        mock_convert.assert_has_calls(expected_calls, any_order=True)
        self.assertEqual(mock_convert.call_count, 2)


    @patch("kernpy.__main__.kern_to_ekern")
    def test_kern2ekern_single_file(self, mock_convert):
        file = self.create_file(self.temp_path / "file.krn")
        args = mock.Mock(input_path=str(file), output_path=None, recursive=False, verbose=1)

        handle_kern2ekern(args)

        mock_convert.assert_called_once_with(str(file), str(file.with_suffix(".ekrn")))

    @patch("kernpy.__main__.kern_to_ekern")
    def test_kern2ekern_recursive_mixed(self, mock_convert):
        f1 = self.create_file(self.nested_dir / "score.krn")
        f2 = self.create_file(self.nested_dir / "part.kern")

        args = mock.Mock(input_path=str(self.temp_path), output_path=None, recursive=True, verbose=1)

        handle_kern2ekern(args)

        expected_calls = [
            mock.call(str(f1), str(f1.with_suffix(".ekrn"))),
            mock.call(str(f2), str(f2.with_suffix(".ekrn")))
        ]
        mock_convert.assert_has_calls(expected_calls, any_order=True)
        self.assertEqual(mock_convert.call_count, 2)


    @patch("kernpy.__main__.polish_scores.download_polish_dataset.main")
    def test_polish_exporter_minimal(self, mock_polish_main):
        args = mock.Mock(
            input_directory=str(self.temp_path),
            output_directory=str(self.temp_path / "out"),
            kern_spines_filter="3",
            kern_type="ekrn",
            remove_empty_dirs=True,
            instrument=None,
            verbose=1
        )

        handle_polish_exporter(args)

        mock_polish_main.assert_called_once_with(
            input_directory=args.input_directory,
            output_directory=args.output_directory,
            kern_spines_filter="3",
            exporter_kern_type="ekrn",
            remove_empty_directories=True,
        )

    @patch("kernpy.__main__.polish_scores.download_polish_dataset.main")
    def test_polish_exporter_with_instrument(self, mock_polish_main):
        args = mock.Mock(
            input_directory=str(self.temp_path),
            output_directory=str(self.temp_path / "out"),
            kern_spines_filter=None,
            kern_type="krn",
            remove_empty_dirs=False,
            instrument="piano",
            verbose=2
        )

        handle_polish_exporter(args)
        mock_polish_main.assert_called_once()


if __name__ == "__main__":
    unittest.main()
