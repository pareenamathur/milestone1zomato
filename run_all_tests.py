import unittest
import sys

def run_tests():
    """Discover and run all tests in the project."""
    print("Discovering and running all unit tests...")
    
    loader = unittest.TestLoader()
    suite = loader.discover('tests', pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    if not result.wasSuccessful():
        sys.exit(1)

if __name__ == "__main__":
    run_tests()
