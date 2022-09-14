FROM 812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base:6839-main

RUN apt-get install curl -y

# Get miniconda
RUN curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh --output miniconda.sh
ENV CONDA_DIR /opt/conda
RUN bash miniconda.sh -b -p /opt/conda
ENV PATH=$CONDA_DIR/bin:$PATH

# Get Mamba
RUN conda install mamba -n base -c conda-forge

# Get MegaHIT and Quast
RUN mamba create -y -n kalign python=3.8
RUN mamba install -y -n kalign -c bioconda kalign3
ENV KALIGN_ENV $CONDA_DIR/envs/kalign/bin

# Create symlink
RUN ln -s $KALIGN_ENV/kalign /root/kalign

# STOP HERE:
# The following lines are needed to ensure your build environement works
# correctly with latch.
RUN python3 -m pip install --upgrade latch
COPY wf /root/wf
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
WORKDIR /root
