#!/usr/bin/env python3
"""
Main entry point for Repair Company Management System.
Run this file to start the application.
"""

import sys
import os

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def main():
    """Main entry point function."""
    print("=" * 50)
    print("REPAIR COMPANY - MANAGEMENT SYSTEM v1.0.0")
    print("=" * 50)
    
    while True:  
        print("\n" + "=" * 50)
        print("MAIN MENU")
        print("=" * 50)
        print("1. 📊 Demonstration Mode")
        print("2. 🖥️  Interactive Mode (CLI)")
        print("3. ✅ Run All Tests")
        print("4. 🧪 Run Specific Test Module")
        print("5. 📈 Check Test Coverage (85%+)")  
        print("0. ❌ Exit")
        
        try:
            choice = input("\nEnter mode number: ").strip()
            
            if choice == "1":
                print("\n" + "=" * 50)
                print("STARTING DEMONSTRATION MODE")
                print("=" * 50)
                try:
                    from src.main import RepairCompanyDemo
                    demo = RepairCompanyDemo()
                    demo.demonstrate_all_functionality()
                    print("\n" + "=" * 50)
                    print("DEMONSTRATION COMPLETED")
                    print("Returning to main menu...")
                    print("=" * 50)
                except ImportError as e:
                    print(f"\n❌ Import error: {e}")
                    print("Please check that all __init__.py files exist.")
                except Exception as e:
                    print(f"\n❌ Error in demonstration: {e}")
                
            elif choice == "2":
                print("\n" + "=" * 50)
                print("STARTING INTERACTIVE MODE")
                print("=" * 50)
                try:
                    from src.main_interactive import InteractiveRepairCompany
                    company = InteractiveRepairCompany()
                    company.run_interactive_system()
                    print("\n" + "=" * 50)
                    print("INTERACTIVE MODE COMPLETED")
                    print("Returning to main menu...")
                    print("=" * 50)
                except ImportError as e:
                    print(f"\n❌ Import error: {e}")
                    print("Please check that all __init__.py files exist.")
                except Exception as e:
                    print(f"\n❌ Error in interactive mode: {e}")
                
            elif choice == "3":
                print("\n" + "=" * 50)
                print("RUNNING ALL TESTS")
                print("=" * 50)
                try:
                    import unittest
                    loader = unittest.TestLoader()
                    suite = loader.discover('tests', pattern='test_*.py')
                    runner = unittest.TextTestRunner(verbosity=2)
                    result = runner.run(suite)
                    print("\n" + "=" * 50)
                    print("TESTS COMPLETED")
                    print("Returning to main menu...")
                    print("=" * 50)
                except Exception as e:
                    print(f"\n❌ Error running tests: {e}")
                
            elif choice == "4":
                print("\n" + "=" * 50)
                print("AVAILABLE TEST MODULES")
                print("=" * 50)
                print("1. test_models.py")
                print("2. test_finance.py")
                print("3. test_services.py")
                print("4. test_security.py")
                print("5. test_utils.py")
                print("6. test_integration.py")
                print("7. test_exceptions.py")
                print("8. test_models_comprehensive.py")
                print("9. test_input_handler.py")
                print("0. Back to main menu")
                
                try:
                    test_choice = input("\nSelect test module (0 to cancel): ").strip()
                    
                    if test_choice == "0":
                        continue
                    
                    test_map = {
                        '1': 'test_models',
                        '2': 'test_finance',
                        '3': 'test_services',
                        '4': 'test_security',
                        '5': 'test_utils',
                        '6': 'test_integration',
                        '7': 'test_exceptions',
                        '8': 'test_models_comprehensive',
                        '9': 'test_input_handler'
                    }
                    
                    if test_choice in test_map:
                        selected_test = test_map[test_choice]
                        print(f"\n" + "=" * 50)
                        print(f"RUNNING TEST MODULE: {selected_test}")
                        print("=" * 50)
                        
                        try:
                            import unittest
                            # Try to load test module
                            test_module = f'tests.{selected_test}'
                            suite = unittest.defaultTestLoader.loadTestsFromName(test_module)
                            if suite.countTestCases() == 0:
                                # If that fails, try loading from file
                                test_file = f'tests/{selected_test}.py'
                                suite = unittest.defaultTestLoader.discover('tests', pattern=f'{selected_test}.py')
                            
                            runner = unittest.TextTestRunner(verbosity=2)
                            runner.run(suite)
                            
                            print("\n" + "=" * 50)
                            print("TEST COMPLETED")
                            print("Returning to main menu...")
                            print("=" * 50)
                            
                        except ImportError as e:
                            print(f"\n❌ Import error: {e}")
                            print("Please check that the test file exists.")
                        except Exception as e:
                            print(f"\n❌ Error running tests: {e}")
                            
                    else:
                        print("\n❌ Invalid test selection.")
                        
                except KeyboardInterrupt:
                    print("\n\nTest selection cancelled.")
                    continue
                except Exception as e:
                    print(f"\n❌ Error in test selection: {e}")
                
            elif choice == "5":
                print("\n" + "=" * 50)
                print("CHECKING TEST COVERAGE (85% minimum)")
                print("=" * 50)
                
                try:
                    # Check if coverage module exists
                    import importlib
                    importlib.import_module('coverage')
                    
                    # Try to run check_coverage.py if it exists
                    coverage_script = "check_coverage.py"
                    if os.path.exists(coverage_script):
                        import subprocess
                        result = subprocess.run(
                            [sys.executable, coverage_script],
                            capture_output=True,
                            text=True
                        )
                        
                        print(result.stdout)
                        if result.stderr:
                            print("Errors:", result.stderr)
                    else:
                        # Run coverage directly
                        import subprocess
                        print("Running coverage report...")
                        result = subprocess.run(
                            ['coverage', 'run', '-m', 'pytest'],
                            capture_output=True,
                            text=True
                        )
                        
                        # Generate report
                        report_result = subprocess.run(
                            ['coverage', 'report', '-m'],
                            capture_output=True,
                            text=True
                        )
                        
                        print("Test Results:")
                        print(result.stdout)
                        if result.stderr:
                            print("Test Errors:", result.stderr)
                        
                        print("\nCoverage Report:")
                        print(report_result.stdout)
                        if report_result.stderr:
                            print("Coverage Errors:", report_result.stderr)
                            
                except ImportError:
                    print("❌ Coverage module not installed.")
                    print("Install it with: pip install coverage")
                except Exception as e:
                    print(f"\n❌ Error checking coverage: {e}")
                
                input("\nPress Enter to continue...")
                
            elif choice == "0":
                print("\n" + "=" * 50)
                print("Thank you for using Repair Company System!")
                print("Goodbye!")
                print("=" * 50)
                sys.exit(0)
                
            else:
                print("\n❌ Invalid choice. Please enter 0-5.")
                
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
            print("Returning to main menu...")
            continue
        except EOFError:
            print("\n\nEnd of input detected.")
            print("Exiting program. Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            print("Returning to main menu...")

if __name__ == "__main__":
    main()