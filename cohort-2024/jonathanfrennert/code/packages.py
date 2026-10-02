# Importing modules from different packages
import module_a.utils as analysis_utils
import module_b.utils as frontend_utils

# Using functions from the imported modules
data_result = analysis_utils.analyze_data("Sample Data")
view_result = frontend_utils.render_view("Home Page")

# Print the results
print(data_result)  # Output: Analyzing data: Sample Data
print(view_result)  # Output: Rendering view: Home Page
