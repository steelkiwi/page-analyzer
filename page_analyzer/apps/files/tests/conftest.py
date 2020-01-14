import tempfile
import pytest

from PIL import Image


@pytest.fixture()
def temp_image(suffix='.png'):
    image = Image.new('RGB', (100, 100))
    tmp_file = tempfile.NamedTemporaryFile(suffix=suffix)
    image.save(tmp_file)
    tmp_file.seek(0)

    return tmp_file


@pytest.fixture()
def temp_file(suffix='.dat'):
    tmp_file = tempfile.NamedTemporaryFile(suffix=suffix)
    tmp_file.seek(0)

    return tmp_file
