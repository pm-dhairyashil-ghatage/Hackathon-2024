import streamlit as st
import subprocess
import os
import concurrent.futures

script_path = f"{os.getcwd()}/interact.expect"
index_dict = {"Prebid.js": 5, "OW prebid Fork": 6, "Both repo": 8, "Confluence data": 7}
reverse_index_dict = {2: "Prebid.js", 3: "OW prebid Fork"}

default_auth_key = "eyJhbGciOiJIUzI1NiJ9.eyJkYXRhIjoidjFfNjkyNV8xMTIxNzg0XzI1MV9UdWUgSnVsIDMwIDEyOjA3OjMxIFVUQyAyMDI0In0.RCzIvqiGZ8Svn213CXmHdpzTxN6sxfNCdLv9dItrntU"
default_mode = "BASIC"
default_question = "in one paragraph, What is price granularity"

st.set_page_config(page_title="PubMatic Code MindMaster", layout="wide")

hide_streamlit_style = """
<style>
footer {
    visibility: hidden;
}
footer:after {
    content: 'Made by Deepanshu'; 
    visibility: visible;
    display: block;
    position: fixed;
    bottom: 0;
    width: 100%;
    text-align: center;
    font-size: 20px;
    padding: 1px;
    background-color: #FFFFFF;
    color: black;
    z-index: 1000;
}
header {
    background-color: rgba(14, 17, 23, 0.5) !important;
    color: white !important;
    padding-left: 20px !important;
    padding-right: 20px !important;
}
main {
    padding-left: 0 !important;
    margin-left: 0 !important;
}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title("Prebid Wikipedia")
st.write("This is an advanced tool to answer your queries about Prebid Code")

index = index_dict.keys()
print("index", index)

suggested_questions_list = [
    "Fetch release notes for OW as per version", "Fetch release notes for OW as per date",
    "Fetch release notes for Prebid as per version", "Fetch release notes for Prebid as per date",
    "New feature in selected release", "Supported platform for given partner",
    "Status of given partner in OpenWrap", "Changes in partner in specific release"
]

ques_select = st.selectbox("Suggested Questions", suggested_questions_list, None, help="Select any question from the suggested list of questions", placeholder="Choose an option", disabled=False, label_visibility="visible")

question = st.text_input("Question", value=default_question)
question = question + " in my code"

print(question)

output_file_name = "final_response.txt"
output_file = f"output/{output_file_name}"

def run_command(command):
    return subprocess.run(command, capture_output=True, text=True)

if st.button('Get Info'):
    placeholder = st.empty()
    placeholder.text("Getting the output, please wait...")
    write = "w"
    append = "a"
    with open(output_file, 'w') as file:
        file.truncate(0)

    cmdPrebid = [script_path, default_auth_key, default_mode, str(5), question, append]
    cmdPrebidFork = [script_path, default_auth_key, default_mode, str(6), question, append]
    cmdLLM = [script_path, default_auth_key, default_mode, str(7), question, append]

    commands = [cmdPrebid, cmdPrebidFork, cmdLLM]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(run_command, commands))

    resultPrebid = results[0]
    resultPrebidFork = results[1]
    resultLLM = results[2]

    result = (
        "\n prebid output \n" + resultPrebid.stdout +
        "\n prebid fork output \n" + resultPrebidFork.stdout +
        "\n LLM output \n" + resultLLM.stdout 
        # "\n prebid errors \n" + resultPrebid.stderr +
        # "\n prebid fork errors \n" + resultPrebidFork.stderr +
        # "\n LLM errors \n" + resultLLM.stderr
    )

    placeholder.empty()
    if os.path.exists(output_file):
        with open(output_file, 'r') as file:
            output_contents = file.read()


    with open(output_file, 'w') as file:
        file.truncate(0) 
        
    question = "Summarize this code in simple 100 words \n" + output_contents
    cmdLLM = [script_path, default_auth_key, default_mode, str(7), question, write]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        result_summary = list(executor.map(run_command, [cmdLLM]))[0]

   

    if resultPrebid.stderr or resultPrebidFork.stderr or resultLLM.stderr:
        st.error("There were errors during execution. See details below.")
        st.error(f"Prebid errors: {resultPrebid.stderr}")
        st.error(f"Prebid fork errors: {resultPrebidFork.stderr}")
        st.error(f"LLM errors: {resultLLM.stderr}")

    if os.path.exists(output_file):
        with open(output_file, 'r') as file:
            contents = file.read()
            output_contents = contents.split('#')[0]
        st.text_area("Output", value=output_contents, height=600)
    else:
        st.error("Output file not found.")
