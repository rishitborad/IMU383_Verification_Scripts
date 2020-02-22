# IMU383_Verification_Scripts
IMU383 - UART Interface Verification Scripts
___
Run IMU383_Verification.py

Need to change UART port/baudrate inside IMU383_Verification.py

# Test Hierarchy
  
    <test_section>
      <test_cases> </test_cases>
    
      <test_cases> </test_cases>
    
                  .
                  .
      <test_cases> </test_cases>
    </test_section>

# To add more test cases
scripts.py file contains all the test cases and their implementation. *test_environment* class 
registers test cases and test sections. This class is responsible for running all the registered test cases and storing the results. Implementation of each test case is inside *test_script* class. 
