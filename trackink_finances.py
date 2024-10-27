import subprocess

def run_program(commands):
    process = subprocess.Popen(
        ['python', 'tracking_finances.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    stdout, stderr = process.communicate(input=commands)
    
    return stdout, stderr

def test_menu_and_input_validation():
    commands = "5\n4\n"
    stdout, stderr = run_program(commands)
    
    assert "Invalid choice. Please select 1, 2, 3, or 4." in stdout
    assert "Thanks for using My Finance!" in stdout

def test_gross_pay_calculation():
    commands = "1\n27.45\n160\n4\n"
    stdout, stderr = run_program(commands)
    
    assert "Gross Pay: $4392.00 (160.0 hours @ $27.45/hr)" in stdout
    assert "Federal tax: $439.20" in stdout
    assert "State tax: $219.60" in stdout
    assert "Social security: $272.30" in stdout
    assert "Net pay: $3460.90" in stdout

def test_revenue_and_expenses():
    commands = "2\npay\n3460.90\ny\nrent\n-2200\nn\n3\n4\n"
    stdout, stderr = run_program(commands)
    
    assert "Revenue: $3460.90 Expenses: $-2200.00 Discretionary: $1260.90" in stdout
    assert "Thanks for using My Finance!" in stdout

if __name__ == "__main__":
    test_menu_and_input_validation()
    test_gross_pay_calculation()
    test_revenue_and_expenses()
    print("All tests passed.")
