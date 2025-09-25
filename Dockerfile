# Base image
FROM ubuntu:16.04

# Set non-interactive mode
ENV DEBIAN_FRONTEND=noninteractive

# Update and install system basics
RUN apt-get update && apt-get install -y \
    sudo wget curl git build-essential cmake unzip pkg-config \
    libx11-dev libgl1-mesa-glx libglu1-mesa-dev \
    software-properties-common \
    libssl-dev zlib1g-dev libbz2-dev libreadline-dev \
    libsqlite3-dev llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Compile and install Python 3.6
RUN cd /usr/src && \
    wget https://www.python.org/ftp/python/3.6.15/Python-3.6.15.tgz && \
    tar xzf Python-3.6.15.tgz && \
    cd Python-3.6.15 && \
    ./configure --enable-optimizations && \
    make altinstall

# Upgrade pip
RUN python3.6 -m pip install --upgrade pip

# Install HDF5, OpenEXR, GLFW, Xorg, etc.
RUN apt-get update && apt-get install -y \
    libhdf5-10 libhdf5-serial-dev libhdf5-dev libhdf5-cpp-11 \
    libopenexr-dev zlib1g-dev openexr \
    xorg-dev libglfw3-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set Python3.6 as default
RUN update-alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3.6 1

RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    libxvidcore-dev \
    libx264-dev \
    libgtk-3-dev \
    libatlas-base-dev \
    gfortran \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install CMake >= 3.18 (precompilado)
RUN wget https://github.com/Kitware/CMake/releases/download/v3.21.0/cmake-3.21.0-linux-x86_64.sh \
    && chmod +x cmake-3.21.0-linux-x86_64.sh \
    && ./cmake-3.21.0-linux-x86_64.sh --skip-license --prefix=/usr/local \
    && rm cmake-3.21.0-linux-x86_64.sh  

# Install Python packages from requirements
COPY requirements.txt /tmp/
RUN python3 -m pip install -r /tmp/requirements.txt

# Set workdir
WORKDIR /workspace

# Default command
CMD ["/bin/bash"]
