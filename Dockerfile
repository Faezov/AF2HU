# Start from an official Python image
FROM python:3.8-slim

# Install system-level dependencies
RUN apt-get update && apt-get install -y wget

# Set a working directory
WORKDIR /app

# Copy your Streamlit script (and any other necessary files) to the container
COPY ./alphafold_streamlit_app.py /app/

# Install Python libraries
RUN pip install streamlit

# Install colabfold and other related dependencies
RUN pip install 'colabfold[alphafold-minus-jax] @ git+https://github.com/sokrypton/ColabFold' && \
    pip install dm-haiku && \
    ln -s /usr/local/lib/python3.8/dist-packages/colabfold colabfold && \
    ln -s /usr/local/lib/python3.8/dist-packages/alphafold alphafold

# Patch for jax > 0.3.25
RUN sed -i 's/weights = jax.nn.softmax(logits)/logits=jnp.clip(logits,-1e8,1e8);weights=jax.nn.softmax(logits)/g' alphafold/model/modules.py

# Install conda for amber and hhsuite
RUN wget -qnc https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-Linux-x86_64.sh && \
    bash Mambaforge-Linux-x86_64.sh -bfp /usr/local && \
    mamba config --set auto_update_conda false

# Install hhsuite and amber (adjust as needed)
RUN mamba install -y -c conda-forge -c bioconda kalign2=2.04 hhsuite=3.3.0 openmm=7.7.0 python=3.8 pdbfixer

# Set Streamlit's settings
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV STREAMLIT_SERVER_PORT=8501

# Run Streamlit app
CMD ["streamlit", "run", "/app/alphafold_streamlit_app.py"]

