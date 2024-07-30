import streamlit as st
import subprocess, os

# Set the page configuration - title and layout mode
st.set_page_config(page_title="PubMatic Code MindMaster", layout="wide")

hide_streamlit_style = """
            <style>
            /* Hide the default Streamlit footer */
            footer {
                visibility: hidden;
            }
            /* Custom footer content */
            footer:after {
                content: 'Made by Deepanshu'; 
                visibility: visible;
                display: block;
                position: fixed; /* Change to fixed */
                bottom: 0; /* Align to the bottom of the viewport */
                width: 100%;
                text-align: center;
                font-size: 20px; /* Increased font size for prominence */
                padding: 1px; /* Adjust padding as needed */
                background-color: #FFFFFF; /* Change background color */
                color: black; /* Change text color */
                z-index: 1000; /* Ensure it's above other content */
            }
            /* Adjusted header styling for semi-transparent background and asymmetric padding */
            header {
                background-color: rgba(14, 17, 23, 0.5) !important; /* Semi-transparent background */
                color: white !important; /* Header text color */
                padding-left: 20px !important; /* More padding on the left */
                padding-right: 20px !important; /* Less padding on the right */
            }
            /* Remove any additional padding or margin that may be on the left */
            main {
                padding-left: 0 !important;
                margin-left: 0 !important;
            }
            /* Additional selectors might be required to target the correct element */
            /* Use browser developer tools to find the right classes to target */

            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

# Display an image at the top of the page
st.title("Prebid Wiki")
st.write("This is a Advanced tool to answer your queries about Prebid Code")

# Define default values for the inputs
default_auth_key = "eyJhbGciOiJIUzI1NiJ9.eyJkYXRhIjoidjFfNjkyNV8xMTIxNzg0XzI1MV9UdWUgSnVsIDMwIDEyOjA3OjMxIFVUQyAyMDI0In0.RCzIvqiGZ8Svn213CXmHdpzTxN6sxfNCdLv9dItrntU"
default_mode = "ADVANCED"
index_dict = {"Prebid_1.js": 5,"Prebid.js": 6,"LLM Data": 7}
default_question = "in one paragraph, how does publisher allowlist inline upload api work?"

# Create input fields in the Streamlit app
question = st.text_input("Question", value=default_question)
question = question + " in my code"


print(question)

selected_value_for_cmd = "6"  # Default value if no checkbox is selected
output_file_name = selected_value_for_cmd + "final_response.txt"

output_file = f"/home/dhirajdarakhe/Documents/fantastic6/{output_file_name}"


# Absolute path to the script
script_path = "/home/dhirajdarakhe/Documents/fantastic6/interact.expect"

# Button to trigger the script
if st.button('Get Info'):
    placeholder = st.empty()
    placeholder.text("Getting the output, please wait...")

    with open(output_file, 'w') as file:
        file.truncate(0)

    # Change the current working directory
    os.chdir('/home/dhirajdarakhe/Documents/fantastic6')
    
    # Construct the command to run the script using the absolute path
    cmd = [script_path, default_auth_key, default_mode,selected_value_for_cmd, question]

    print("Current working directory before subprocess call:", os.getcwd())

    # Execute the command and capture the output
    result = subprocess.run(cmd, capture_output=True, text=True)
    

    # Replace the temporary message with the actual content
    placeholder.empty()

    # Check for errors in script execution
    if result.stderr:
        st.error(f"Error: {result.stderr}")
    # else:
    #     # Get the numeric value corresponding to the selected key from index_dict
    #     numeric_value = index_dict[selected_keys[0]]

    #     # Assuming output_file_name is the original file name that includes the key
    #     # For demonstration, let's say it's something like "heimdall_final_response.txt"

    #     # Replace the selected key in the file name with its numeric value from index_dict
    #     modified_file_name = output_file_name.replace(str(selected_keys[0]), str(numeric_value))

    #     # Construct the full path to the file
    #     output_file = f"/home/dhirajdarakhe/Documents/fantastic6/{modified_file_name}"

        # If script ran successfully, read and display the contents of the output file
    if os.path.exists(output_file):
        print(output_file)
        with open(output_file, 'r') as file:
            output_contents = file.read()
            # Adjust the height of the text area dynamically based on the output content length
            #dynamic_height = min(len(output_contents.split('\n')) * 20, 600)
        st.text_area("Output", value=output_contents, height=600)
    else:
        st.error("Output file not found.")
