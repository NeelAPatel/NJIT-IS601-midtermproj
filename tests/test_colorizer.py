''' Tests the Colorizer Add-on'''

import logging
import pytest
from app.Colorizer import Colorizer

# Fixture to initialize Colorizer with different environment settings
@pytest.fixture(params=[
    {'LOG_COLORED': 'COLOR'},  # Test with colored logs enabled
    {'LOG_COLORED': 'DEFAULT'},  # Test with default settings (no colored logs)
    {}  # Test with empty settings
])
def colorizer(request):
    ''' Fixture for colorizer'''
    return Colorizer(request.param)

# Test initialization and attribute setting
def test_colorizer_initialization(colorizer):
    '''Tests colorizer addon initialization'''
    assert isinstance(colorizer, Colorizer)
    assert hasattr(colorizer, 'env_settings')

# Test formatting without color
def test_formatting_without_color(colorizer):
    '''Tests colorizer addon with colored enabled'''
    if colorizer.env_settings.get('LOG_COLORED', '').upper() != 'COLOR':
        record = logging.LogRecord(name='test', level=logging.INFO, pathname=None, lineno=None, msg='Test message', args=(), exc_info=None)
        formatted_message = colorizer.format(record)
        assert '\033' not in formatted_message  # No color codes should be present

# Test formatting with color
def test_formatting_with_color(colorizer):
    '''Tests colorizer addon with colored disabled'''
    if colorizer.env_settings.get('LOG_COLORED', '').upper() == 'COLOR':
        record = logging.LogRecord(name='test', level=logging.INFO, pathname=None, lineno=None, msg='Test message', args=(), exc_info=None)
        formatted_message = colorizer.format(record)
        assert '\033' in formatted_message  # Color codes should be present
