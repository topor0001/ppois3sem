from rectangle import Rectangle, rectangle_from_string, create_rectangle_default
from set import Set, set_from_string, create_empty_set, create_set_from_elements
import sys
import os
import subprocess

def display_menu():
    print("\n" + "="*50)
    print(" RECTANGLE AND SET CLASSES DEMO")
    print("="*50)
    print("1. Work with Rectangle class")
    print("2. Work with Set class")
    print("3. Run Rectangle unit tests")
    print("4. Run Set unit tests")
    print("5. Run all unit tests")
    print("6. Check test coverage (85% minimum requirement)")
    print("7. Exit")
    print("="*50)
    print("Choose option: ", end="")

def get_integer_input(prompt):
    while True:
        try:
            value = input(prompt)
            return int(value)
        except ValueError:
            print("❌ Error! Please enter an integer.")

def get_element_input():
    print("Choose element type:")
    print("1. Empty set")
    print("2. String element")
    print("3. Number element")
    elem_type = input("Choose element type (1-3): ")
    if elem_type == "1":
        return create_empty_set()
    elif elem_type == "2":
        value = input("Enter string value: ")
        return value
    elif elem_type == "3":
        value = get_integer_input("Enter number value: ")
        return value
    else:
        print("❌ Invalid element type")
        return None

def rectangle_menu():
    rectangles = []
    while True:
        print("\n" + "="*50)
        print(" RECTANGLE OPERATIONS MENU")
        print("="*50)
        print("1. Create new rectangle")
        print("2. Show all rectangles")
        print("3. Move rectangle")
        print("4. Resize rectangle")
        print("5. Union of two rectangles")
        print("6. Intersection of two rectangles")
        print("7. Increment/decrement rectangle")
        print("8. Compare two rectangles")
        print("9. Create rectangle from string")
        print("10. Convert rectangle to string")
        print("11. Return to main menu")
        print("="*50)
        choice = input("Choose operation: ")

        if choice == "1":
            print("\n--- Creating Rectangle ---")
            x = get_integer_input("Enter x coordinate of bottom-left corner: ")
            y = get_integer_input("Enter y coordinate of bottom-left corner: ")
            width = get_integer_input("Enter rectangle width: ")
            height = get_integer_input("Enter rectangle height: ")
            rect = Rectangle(x, y, width, height)
            rectangles.append(rect)
            print(f"✅ Created rectangle: {rect}")
            print(f"Vertices: {rect.get_vertices()}")

        elif choice == "2":
            print("\n--- Rectangle List ---")
            if not rectangles:
                print("No rectangles created")
            for i, rect in enumerate(rectangles, 1):
                print(f"{i}. {rect}")

        elif choice == "3":
            if not rectangles:
                print("❌ Please create rectangles first")
                continue
            print("\n--- Moving Rectangle ---")
            for i, rect in enumerate(rectangles, 1):
                print(f"{i}. {rect}")
            idx = get_integer_input("Select rectangle number: ") - 1
            if 0 <= idx < len(rectangles):
                dx = get_integer_input("Enter x offset: ")
                dy = get_integer_input("Enter y offset: ")
                rectangles[idx].move(dx, dy)
                print(f"✅ Rectangle moved: {rectangles[idx]}")
            else:
                print("❌ Invalid rectangle number")

        elif choice == "4":
            if not rectangles:
                print("❌ Please create rectangles first")
                continue
            print("\n--- Resizing Rectangle ---")
            for i, rect in enumerate(rectangles, 1):
                print(f"{i}. {rect}")
            idx = get_integer_input("Select rectangle number: ") - 1
            if 0 <= idx < len(rectangles):
                new_width = get_integer_input("Enter new width: ")
                new_height = get_integer_input("Enter new height: ")
                rectangles[idx].resize(new_width, new_height)
                print(f"✅ Size changed: {rectangles[idx]}")
            else:
                print("❌ Invalid rectangle number")

        elif choice == "5":
            if len(rectangles) < 2:
                print("❌ Need at least 2 rectangles")
                continue
            print("\n--- Rectangle Union ---")
            for i, rect in enumerate(rectangles, 1):
                print(f"{i}. {rect}")
            idx1 = get_integer_input("Select first rectangle: ") - 1
            idx2 = get_integer_input("Select second rectangle: ") - 1
            if 0 <= idx1 < len(rectangles) and 0 <= idx2 < len(rectangles):
                union = rectangles[idx1] + rectangles[idx2]
                rectangles.append(union)
                print(f"✅ Created union: {union}")
            else:
                print("❌ Invalid rectangle numbers")

        elif choice == "6":
            if len(rectangles) < 2:
                print("❌ Need at least 2 rectangles")
                continue
            print("\n--- Rectangle Intersection ---")
            for i, rect in enumerate(rectangles, 1):
                print(f"{i}. {rect}")
            idx1 = get_integer_input("Select first rectangle: ") - 1
            idx2 = get_integer_input("Select second rectangle: ") - 1
            if 0 <= idx1 < len(rectangles) and 0 <= idx2 < len(rectangles):
                intersection = rectangles[idx1] - rectangles[idx2]
                rectangles.append(intersection)
                print(f"✅ Created intersection: {intersection}")
            else:
                print("❌ Invalid rectangle numbers")

        elif choice == "7":
            if not rectangles:
                print("❌ Please create rectangles first")
                continue
            print("\n--- Size Change by 1 ---")
            for i, rect in enumerate(rectangles, 1):
                print(f"{i}. {rect}")
            idx = get_integer_input("Select rectangle number: ") - 1
            if 0 <= idx < len(rectangles):
                operation = input("Enter '+' to increase or '-' to decrease: ")
                if operation == '+':
                    new_rect = +rectangles[idx]
                    rectangles.append(new_rect)
                    print(f"✅ Created enlarged rectangle: {new_rect}")
                elif operation == '-':
                    new_rect = -rectangles[idx]
                    rectangles.append(new_rect)
                    print(f"✅ Created reduced rectangle: {new_rect}")
                else:
                    print("❌ Invalid operation")
            else:
                print("❌ Invalid rectangle number")

        elif choice == "8":
            if len(rectangles) < 2:
                print("❌ Need at least 2 rectangles")
                continue
            print("\n--- Rectangle Comparison ---")
            for i, rect in enumerate(rectangles, 1):
                print(f"{i}. {rect}")
            idx1 = get_integer_input("Select first rectangle: ") - 1
            idx2 = get_integer_input("Select second rectangle: ") - 1
            if 0 <= idx1 < len(rectangles) and 0 <= idx2 < len(rectangles):
                rect1 = rectangles[idx1]
                rect2 = rectangles[idx2]
                print(f"Rectangle 1 == Rectangle 2: {rect1 == rect2}")
                print(f"Rectangle 1 != Rectangle 2: {rect1 != rect2}")
            else:
                print("❌ Invalid rectangle numbers")

        elif choice == "9":
            print("\n--- Create Rectangle from String ---")
            print("Format: 'x y width height' (e.g., '1 2 3 4')")
            string_repr = input("Enter rectangle string: ")
            try:
                rect = rectangle_from_string(string_repr)
                rectangles.append(rect)
                print(f"✅ Created rectangle from string: {rect}")
            except Exception as e:
                print(f"❌ Error creating rectangle: {e}")

        elif choice == "10":
            if not rectangles:
                print("❌ Please create rectangles first")
                continue
            print("\n--- Convert Rectangle to String ---")
            for i, rect in enumerate(rectangles, 1):
                print(f"{i}. {rect}")
            idx = get_integer_input("Select rectangle number: ") - 1
            if 0 <= idx < len(rectangles):
                str_repr = rectangles[idx].to_string()
                print(f"✅ String representation: {str_repr}")
            else:
                print("❌ Invalid rectangle number")

        elif choice == "11":
            break
        else:
            print("❌ Invalid option")

def set_menu():
    sets = []
    while True:
        print("\n" + "="*50)
        print(" SET OPERATIONS MENU")
        print("="*50)
        print("1. Create new set")
        print("2. Show all sets")
        print("3. Add element to set")
        print("4. Remove element from set")
        print("5. Union of two sets")
        print("6. Intersection of two sets")
        print("7. Difference of two sets")
        print("8. Check element membership")
        print("9. Build power set")
        print("10. Create set from string")
        print("11. Return to main menu")
        print("="*50)
        choice = input("Choose operation: ")

        if choice == "1":
            print("\n--- Creating Set ---")
            new_set = create_empty_set()
            sets.append(new_set)
            print(f"✅ Created empty set: {new_set}")

        elif choice == "2":
            print("\n--- Set List ---")
            if not sets:
                print("No sets created")
            for i, s in enumerate(sets, 1):
                print(f"{i}. {s} (cardinality: {s.get_cardinality()})")

        elif choice == "3":
            if not sets:
                print("❌ Please create sets first")
                continue
            print("\n--- Adding Element to Set ---")
            for i, s in enumerate(sets, 1):
                print(f"{i}. {s}")
            set_idx = get_integer_input("Select set: ") - 1
            if 0 <= set_idx < len(sets):
                new_element = get_element_input()
                if new_element is not None:
                    sets[set_idx].add_element(new_element)
                    print(f"✅ Element added. Set: {sets[set_idx]}")
            else:
                print("❌ Invalid set number")

        elif choice == "4":
            if not sets:
                print("❌ Please create sets first")
                continue
            print("\n--- Removing Element from Set ---")
            for i, s in enumerate(sets, 1):
                print(f"{i}. {s}")
            set_idx = get_integer_input("Select set: ") - 1
            if 0 <= set_idx < len(sets):
                target_set = sets[set_idx]
                if target_set.is_empty():
                    print("❌ Set is empty")
                    continue
                elements = list(target_set)
                for j, elem in enumerate(elements, 1):
                    print(f"{j}. {elem}")
                elem_idx = get_integer_input("Select element to remove: ") - 1
                if 0 <= elem_idx < len(elements):
                    target_set.remove_element(elements[elem_idx])
                    print(f"✅ Element removed. Set: {target_set}")
                else:
                    print("❌ Invalid element number")
            else:
                print("❌ Invalid set number")

        elif choice == "5":
            if len(sets) < 2:
                print("❌ Need at least 2 sets")
                continue
            print("\n--- Set Union ---")
            for i, s in enumerate(sets, 1):
                print(f"{i}. {s}")
            idx1 = get_integer_input("Select first set: ") - 1
            idx2 = get_integer_input("Select second set: ") - 1
            if 0 <= idx1 < len(sets) and 0 <= idx2 < len(sets):
                union_set = sets[idx1] + sets[idx2]
                sets.append(union_set)
                print(f"✅ Created union: {union_set}")
                print(f"Union cardinality: {union_set.get_cardinality()}")
            else:
                print("❌ Invalid set numbers")

        elif choice == "6":
            if len(sets) < 2:
                print("❌ Need at least 2 sets")
                continue
            print("\n--- Set Intersection ---")
            for i, s in enumerate(sets, 1):
                print(f"{i}. {s}")
            idx1 = get_integer_input("Select first set: ") - 1
            idx2 = get_integer_input("Select second set: ") - 1
            if 0 <= idx1 < len(sets) and 0 <= idx2 < len(sets):
                intersection_set = sets[idx1] * sets[idx2]
                sets.append(intersection_set)
                print(f"✅ Created intersection: {intersection_set}")
                print(f"Intersection cardinality: {intersection_set.get_cardinality()}")
            else:
                print("❌ Invalid set numbers")

        elif choice == "7":
            if len(sets) < 2:
                print("❌ Need at least 2 sets")
                continue
            print("\n--- Set Difference ---")
            for i, s in enumerate(sets, 1):
                print(f"{i}. {s}")
            idx1 = get_integer_input("Select first set (A): ") - 1
            idx2 = get_integer_input("Select second set (B) for A-B: ") - 1
            if 0 <= idx1 < len(sets) and 0 <= idx2 < len(sets):
                difference_set = sets[idx1] - sets[idx2]
                sets.append(difference_set)
                print(f"✅ Created difference: {difference_set}")
                print(f"Difference cardinality: {difference_set.get_cardinality()}")
            else:
                print("❌ Invalid set numbers")

        elif choice == "8":
            if len(sets) < 2:
                print("❌ Need at least 2 sets")
                continue
            print("\n--- Element Membership Check ---")
            for i, s in enumerate(sets, 1):
                print(f"{i}. {s}")
            set_idx = get_integer_input("Select set to check: ") - 1
            elem_idx = get_integer_input("Select element to check (set number): ") - 1
            if (0 <= set_idx < len(sets) and 0 <= elem_idx < len(sets) and
                set_idx != elem_idx):
                element_to_check = sets[elem_idx]
                target_set = sets[set_idx]
                contains = element_to_check in target_set
                print(f"Element {element_to_check} in set {target_set}: {contains}")
                print(f"Check via operator []: {target_set[element_to_check]}")
            else:
                print("❌ Invalid set numbers")

        elif choice == "9":
            if not sets:
                print("❌ Please create sets first")
                continue
            print("\n--- Building Power Set ---")
            for i, s in enumerate(sets, 1):
                print(f"{i}. {s}")
            set_idx = get_integer_input("Select set: ") - 1
            if 0 <= set_idx < len(sets):
                power_set = sets[set_idx].get_power_set()
                sets.append(power_set)
                print(f"✅ Built power set: {power_set}")
                print(f"Power set cardinality: {power_set.get_cardinality()}")
                print("All subsets:")
                for j, subset in enumerate(power_set, 1):
                    print(f" {j}. {subset}")
            else:
                print("❌ Invalid set number")

        elif choice == "10":
            print("\n--- Creating Set from String ---")
            print("Format examples:")
            print(" - Empty set: {}")
            print(" - Set with elements: {a, b, {c}}")
            print(" - Set with numbers: {1, 2, 3}")
            print(" - Mixed set: {hello, 42, {nested}}")
            string_repr = input("Enter string representation of set: ")
            try:
                new_set = set_from_string(string_repr)
                sets.append(new_set)
                print(f"✅ Set created from string: {new_set}")
            except Exception as e:
                print(f"❌ Error creating set: {e}")

        elif choice == "11":
            break
        else:
            print("❌ Invalid option")

def run_tests_rectangle():
    print("\n" + "="*50)
    print(" RUNNING RECTANGLE UNIT TESTS")
    print("="*50)
    try:
        result = subprocess.run([
            sys.executable, "-m", "unittest", "test_rectangle.TestRectangle", "-v"
        ], capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
    except Exception as e:
        print(f"Error running tests: {e}")

def run_tests_set():
    print("\n" + "="*50)
    print(" RUNNING SET UNIT TESTS")
    print("="*50)
    try:
        result = subprocess.run([
            sys.executable, "-m", "unittest", "test_set.TestSet", "-v"
        ], capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
    except Exception as e:
        print(f"Error running tests: {e}")

def run_all_tests():
    """Run all unit tests"""
    print("\n" + "="*50)
    print(" RUNNING ALL UNIT TESTS")
    print("="*50)
    try:
        result = subprocess.run([
            sys.executable, "-m", "unittest", "discover", "-v"
        ], capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
    except Exception as e:
        print(f"Error running tests: {e}")

def run_coverage_check():
    """Check if test coverage meets 85% requirement"""
    print("\n" + "="*50)
    print(" TEST COVERAGE CHECK (85% minimum requirement)")
    print("="*50)
    
    print("Note: This requires 'coverage' package to be installed.")
    print("Install it with: pip install coverage")
    print("\nChecking if coverage is available...")
    
    # Try to run coverage without importing
    try:
        # Check if coverage is available
        result = subprocess.run(
            [sys.executable, "-c", "import coverage; print('coverage available')"],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print("❌ coverage is not installed or not available")
            print("\nTo install coverage:")
            print("1. Open terminal/command prompt")
            print("2. Run: pip install coverage")
            print("3. Try again")
            return
    except:
        print("❌ Could not check coverage installation")
        return
    
    print("✅ coverage is available")
    print("\nRunning tests with coverage measurement...")
    
    # 1. Run tests with coverage
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", 
         "-m", "unittest", "discover"],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("❌ Tests failed!")
        if result.stdout:
            # Show test failures
            for line in result.stdout.split('\n'):
                if 'FAIL' in line or 'ERROR' in line:
                    print(f"  {line}")
        return
    
    # 2. Get coverage percentage
    print("\nCalculating coverage percentage...")
    cov_result = subprocess.run(
        [sys.executable, "-m", "coverage", "report", "--format=total"],
        capture_output=True,
        text=True
    )
    
    if not cov_result.stdout.strip():
        print("❌ Could not get coverage data")
        return
    
    coverage_percent = float(cov_result.stdout.strip())
    
    # 3. Check requirement and show results
    print("\n" + "="*50)
    print("COVERAGE RESULTS")
    print("="*50)
    print(f"📊 Total test coverage: {coverage_percent:.2f}%")
    print(f"📋 Minimum requirement: 85%")
    
    if coverage_percent >= 85:
        print("\n✅ SUCCESS: Coverage ≥ 85% - REQUIREMENT MET!")
        
        # Show detailed report
        print("\nDetailed coverage report:")
        subprocess.run([sys.executable, "-m", "coverage", "report"])
        
        # Generate HTML report
        print("\nGenerating HTML report...")
        subprocess.run([sys.executable, "-m", "coverage", "html"], 
                      capture_output=True, text=True)
        print("✅ HTML report saved in 'htmlcov/' folder")
        print("\nTo view HTML report: open 'htmlcov/index.html' in browser")
        
    else:
        print(f"\n❌ FAILURE: Coverage {coverage_percent:.2f}% < 85%")
        print("   Need to add more tests!")
        
        # Show what's missing
        print("\nMissing coverage details:")
        subprocess.run([sys.executable, "-m", "coverage", "report", "--show-missing"])

def main():
    print("="*60)
    print(" RECTANGLE AND SET CLASSES - COMPLETE IMPLEMENTATION")
    print("="*60)
    print("This program demonstrates:")
    print(" • Rectangle class with geometric operations")
    print(" • Set class with mathematical set operations")
    print(" • Complete unit testing with unittest framework")
    print(" • Interactive testing through menu")
    print(" • Automatic test coverage check (85% minimum)")
    print("="*60)
    
    while True:
        display_menu()
        try:
            choice = input().strip()
            if not choice:
                continue
            choice = int(choice)
        except ValueError:
            print("❌ Invalid input. Please enter a number between 1-7.")
            continue

        if choice == 1:
            rectangle_menu()
        elif choice == 2:
            set_menu()
        elif choice == 3:
            run_tests_rectangle()
        elif choice == 4:
            run_tests_set()
        elif choice == 5:
            run_all_tests()
        elif choice == 6:
            run_coverage_check()
        elif choice == 7:
            print("\n" + "="*50)
            print("Thank you for using the program! Goodbye! 👋")
            print("="*50)
            break
        else:
            print("❌ Invalid option. Please choose 1-7.")

if __name__ == "__main__":
    main()