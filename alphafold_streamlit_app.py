import streamlit as st
import os
import re
import hashlib

def add_hash(x,y):
  return x+"_"+hashlib.sha1(y.encode()).hexdigest()[:5]

st.title('AlphaFold2 Protein Prediction')

# Input protein sequence
query_sequence = st.text_area("Input protein sequence(s):", 
                              'PIAQIHILEGRSDEQKETLIREVSEAISRSLDAPLTSVRVIITEMAKGHFGIGGELASK')
st.markdown("- Use `:` to specify inter-protein chainbreaks for **modeling complexes** (supports homo- and hetro-oligomers). For example '**'PI...SK':'PI...SK'**' for a homodimer")

# Job name
jobname = st.text_input('Job name:', 'myAF2_job')

# Number of models to use
num_relax_options = [0, 1, 5]
num_relax = st.selectbox("Number of top ranked structures to relax using amber:", num_relax_options)

# Template mode
template_mode_options = ["none", "pdb100","custom"]
template_mode = st.selectbox("Template mode:", template_mode_options)

# Submit button
if st.button("Submit"):

    # remove whitespaces
    query_sequence = "".join(query_sequence.split())

    basejobname = "".join(jobname.split())
    basejobname = re.sub(r'\W+', '', basejobname)
    jobname = add_hash(basejobname, query_sequence)

    # make directory to save results
    os.makedirs(jobname, exist_ok=True)

    # save queries
    queries_path = os.path.join(jobname, f"{jobname}.csv")
    with open(queries_path, "w") as text_file:
      text_file.write(f"id,sequence\n{jobname},{query_sequence}")

    if template_mode == "custom":
        custom_template_path = os.path.join(jobname,f"template")
        os.makedirs(custom_template_path, exist_ok=True)
        uploaded = st.file_uploader("Upload your templates:", type=["pdb", "cif"])
        if uploaded:
            with open(os.path.join(custom_template_path, uploaded.name), 'wb') as f:
                f.write(uploaded.getvalue())

    st.write("Jobname:", jobname)
    st.write("Sequence:", query_sequence)
    st.write("Length:", len(query_sequence.replace(":","")))

