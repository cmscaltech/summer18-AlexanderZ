FROM ubuntu:16.04

ARG python=2.7
ENV PYTHON_VERSION=${python}

# Update the sources list
RUN apt-get update


RUN apt-get update && apt-get install -y --no-install-recommends \
                build-essential \
                git \
                curl \
                nano \
                wget \
                ca-certificates \
                dialog \
                cmake \
                vim \
                net-tools \
                build-essential \
                python${PYTHON_VERSION} \
                python${PYTHON_VERSION}-dev
                    
RUN ln -s /usr/bin/python${PYTHON_VERSION} /usr/bin/python

RUN curl -O https://bootstrap.pypa.io/get-pip.py && \
    python get-pip.py && \
    rm get-pip.py

# intall useful and/or required Python libraries to run your script
RUN pip install matplotlib \
                seaborn \
                pandas \
                numpy \
                scipy \
                sklearn \
                python-dateutil \
                scikit-optimize

# download root
RUN mkdir root_download && \
    cd root_download && \
    git clone http://github.com/root-project/root.git && \
    mkdir root_build

RUN apt-get update && apt-get install -y --no-install-recommends \
                libjpeg-dev \
                libpng-dev \
                lzma \
                liblz4-tool \
                libx11-dev \
                libxpm-dev \
                libxft-dev \
                libxext-dev

# install root
RUN cd root_download/root_build && \
    cmake ../root && \
    cmake --build . -- -j8
RUN cd root_download/root_build && \
    /bin/bash -c "source ./bin/thisroot.sh"

# install pythia
RUN cd /root_download && \
    wget http://home.thep.lu.se/~torbjorn/pythia8/pythia8235.tgz && \
    tar xfz pythia8235.tgz && \
    cd pythia8235 && \
    ./configure && \
    make

RUN git clone https://github.com/quantummind/surf2018.git

ENV WorkHOME=/surf2018
RUN cd /surf2018/pythia_space && \
    make PYTHIA8_HOME=/root_download/pythia8235
WORKDIR /surf2018
# ENTRYPOINT ["python"]
# CMD ["master.py", "-c tune_config.json"]