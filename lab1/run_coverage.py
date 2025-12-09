import subprocess
import sys

def main():
    print("=" * 50)
    print("TEST COVERAGE CHECK (85% minimum)")
    print("=" * 50)
    print("\n1. Running tests with coverage...")
    result = subprocess.run(
        [sys.executable, "-m", "coverage", "run", 
         "-m", "unittest", "discover"],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("❌ Tests failed!")
        print(result.stdout)
        return 1
    
    print("\n2. Calculating coverage...")
    cov_result = subprocess.run(
        [sys.executable, "-m", "coverage", "report", "--format=total"],
        capture_output=True,
        text=True
    )
    
    if not cov_result.stdout.strip():
        print("❌ Could not get coverage data")
        return 1
    
    coverage_percent = float(cov_result.stdout.strip())
    
    print("\n3. Checking requirement (85% minimum)...")
    print(f"📊 Total test coverage: {coverage_percent:.2f}%")
    
    if coverage_percent >= 85:
        print("✅ SUCCESS: Coverage ≥ 85% - REQUIREMENT MET!")
        

        print("\n📋 Detailed coverage report:")
        subprocess.run([sys.executable, "-m", "coverage", "report"])
        
        return 0
    else:
        print(f"❌ FAILURE: Coverage {coverage_percent:.2f}% < 85%")
        print("   Need to add more tests!")
        
   
        print("\n⚠️ Missing coverage:")
        subprocess.run([sys.executable, "-m", "coverage", "report", "--show-missing"])
        
        return 1

if __name__ == "__main__":
    sys.exit(main())