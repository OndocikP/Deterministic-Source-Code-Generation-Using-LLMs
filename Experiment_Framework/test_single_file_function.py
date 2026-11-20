#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script for the test_single_file function.
This script demonstrates how the test_single_file function works.
"""

import os
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from Experiment_Framework.funcion.tests.pythone_tests import test_single_file, review_file_hed
from Experiment_Framework.funcion.file_manager import load_setup


def test_function_basic():
    """Test the basic functionality of test_single_file."""
    
    print("=" * 70)
    print("Test 1: Basic functionality test")
    print("=" * 70)
    
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a test Python file
        test_file_path = os.path.join(temp_dir, "is_even.py")
        test_code = """def is_even_number(n):
    return n % 2 == 0
"""
        with open(test_file_path, "w") as f:
            f.write(test_code)
        
        # Create test data
        test_data = {
            "function": "is_even_number",
            "2": "True",
            "3": "False",
            "0": "True",
            "-4": "True",
            "11": "False",
        }
        
        # Run the test
        result = test_single_file(test_data, test_file_path)
        
        # Display results
        print(f"\nFile name: {result[0]}")
        print(f"Code Identity Score: {result[1]}")
        print(f"AST Structure Score: {result[2]}")
        print(f"Behavioral Equivalence Score: {result[3]}")
        
        # Verify results structure
        assert len(result) == 4, f"Expected result length 4, got {len(result)}"
        assert result[0] == "is_even.py", f"Expected file name 'is_even.py', got {result[0]}"
        print("\n✓ Test passed: Result structure is correct")
        print(f"✓ Expected return format: {review_file_hed()}")
        print(f"✓ Actual return: {result}")


def test_function_with_actual_test_data():
    """Test with real test data from the project."""
    
    print("\n" + "=" * 70)
    print("Test 2: Testing with actual project test data")
    print("=" * 70)
    
    # Path to the test data file
    test_data_path = Path(PROJECT_ROOT) / "Evaluations" / "Prompts" / "is_even_number" / "tests_data.txt"
    
    if not test_data_path.exists():
        print(f"⚠ Test data file not found: {test_data_path}")
        print("Skipping this test.")
        return
    
    # Load test data
    test_data = load_setup(str(test_data_path))
    print(f"\nLoaded test data: {test_data}")
    
    # Create a temporary test file
    with tempfile.TemporaryDirectory() as temp_dir:
        test_file_path = os.path.join(temp_dir, "test_implementation.py")
        test_code = """def is_even_number(n):
    return n % 2 == 0
"""
        with open(test_file_path, "w") as f:
            f.write(test_code)
        
        # Run the test
        result = test_single_file(test_data, test_file_path)
        
        # Display results
        print(f"\nFile name: {result[0]}")
        print(f"Code Identity Score: {result[1]}")
        print(f"AST Structure Score: {result[2]}")
        print(f"Behavioral Equivalence Score: {result[3]}")
        
        # Verify behavioral test passed
        behavioral_score = float(result[3])
        print(f"\n✓ Behavioral equivalence score: {behavioral_score:.2f}")
        if behavioral_score >= 0.8:
            print("✓ Test passed: Good behavioral equivalence")
        else:
            print("⚠ Warning: Lower behavioral equivalence score")


def test_function_invalid_file():
    """Test with an invalid file path."""
    
    print("\n" + "=" * 70)
    print("Test 3: Testing with invalid file path")
    print("=" * 70)
    
    test_data = {
        "function": "is_even_number",
        "2": "True",
    }
    
    # Use a non-existent file
    result = test_single_file(test_data, "/non/existent/file.py")
    
    print(f"\nFile name: {result[0]}")
    print(f"Code Identity Score: {result[1]}")
    print(f"AST Structure Score: {result[2]}")
    print(f"Behavioral Equivalence Score: {result[3]}")
    
    # Verify all scores are 0.00
    assert result[1] == "0.00", "Expected Code Identity score to be 0.00"
    assert result[2] == "0.00", "Expected AST Structure score to be 0.00"
    assert result[3] == "0.00", "Expected Behavioral Equivalence score to be 0.00"
    print("\n✓ Test passed: Invalid file returns all 0.00 scores")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("Testing test_single_file function")
    print("=" * 70)
    
    test_function_basic()
    test_function_with_actual_test_data()
    test_function_invalid_file()
    
    print("\n" + "=" * 70)
    print("All tests completed successfully!")
    print("=" * 70)
