#!/usr/bin/env python
"""Test runner script for Trip Planning Assistant."""

import sys
import unittest
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))


def run_tests(verbosity=2, pattern='test_*.py'):
    """
    Run all tests in the tests directory.
    
    Args:
        verbosity: Verbosity level for test output (0-2)
        pattern: Pattern for test file discovery
    
    Returns:
        TestResult object
    """
    loader = unittest.TestLoader()
    start_dir = str(Path(__file__).parent)
    suite = loader.discover(start_dir, pattern=pattern)
    
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)
    
    return result


def run_specific_test(test_module, test_class=None, test_method=None):
    """
    Run a specific test module, class, or method.
    
    Args:
        test_module: Module name (e.g., 'test_config')
        test_class: Optional class name (e.g., 'TestUserPreferences')
        test_method: Optional method name (e.g., 'test_creation')
    
    Returns:
        TestResult object
    """
    if test_method and test_class:
        test_name = f"{test_module}.{test_class}.{test_method}"
    elif test_class:
        test_name = f"{test_module}.{test_class}"
    else:
        test_name = test_module
    
    suite = unittest.TestLoader().loadTestsFromName(test_name)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == '--help':
            print("""
Test Runner for Trip Planning Assistant

Usage:
    python tests/run_tests.py                    # Run all tests
    python tests/run_tests.py test_config        # Run specific test module
    python tests/run_tests.py --coverage         # Run with coverage (if installed)
    python tests/run_tests.py --quiet            # Run with minimal output
            """)
            sys.exit(0)
        elif sys.argv[1] == '--quiet':
            result = run_tests(verbosity=0)
        elif sys.argv[1] == '--coverage':
            try:
                import coverage
                cov = coverage.Coverage()
                cov.start()
                
                result = run_tests(verbosity=2)
                
                cov.stop()
                cov.save()
                
                print("\n" + "="*70)
                print("COVERAGE REPORT")
                print("="*70)
                cov.report()
                cov.html_report(directory='htmlcov')
                print("HTML coverage report generated in htmlcov/")
            except ImportError:
                print("Coverage module not installed. Install with: pip install coverage")
                sys.exit(1)
        else:
            # Assume it's a test module name
            result = run_specific_test(sys.argv[1])
    else:
        result = run_tests(verbosity=2)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
