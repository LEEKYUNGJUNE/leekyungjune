FROM ubuntu:16.04
MAINTAINER Gihyun Yoon <gih2yun@mindslab.ai>

# install packages

ENV MAUM_VERSION 0.13
LABEL ai.mindslab.maum.version="${MAUM_VERSION}"
ENV DOCKER_MINDS_BUILD="maum"

LABEL com.nvidia.volumes.needed="nvidia_driver"

RUN NVIDIA_GPGKEY_SUM=d1be581509378368edeec8c1eb2958702feedf3bc3d17011adbf24efacce4ab5 && \
    NVIDIA_GPGKEY_FPR=ae09fe4bbd223a84b2ccfce3f60f4b3d7fa2af80 && \
    apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/7fa2af80.pub && \
    apt-key adv --export --no-emit-version -a $NVIDIA_GPGKEY_FPR | tail -n +5 > cudasign.pub && \
    echo "$NVIDIA_GPGKEY_SUM  cudasign.pub" | sha256sum -c --strict - && rm cudasign.pub && \
    echo "deb http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64 /" > /etc/apt/sources.list.d/cuda.list

ENV CUDA_VERSION 8.0.61
LABEL com.nvidia.cuda.version="${CUDA_VERSION}"
ENV CUDA_PKG_VERSION=$CUDA_VERSION-1
ENV CUDA_PKG_VERSION2=$CUDA_VERSION.1-1

RUN sed -i 's/archive.ubuntu.com/ftp.daum.net/g' /etc/apt/sources.list

RUN apt-get update && apt-get install -y curl

RUN curl -sL https://deb.nodesource.com/setup_6.x | bash -

RUN apt-get update && apt-get install -y --no-install-recommends \
      git sudo \
      gcc-4.8 g++-4.8 gcc g++ gcc-5 g++-5 \
      make cmake \
      autoconf automake libtool \
      python-pip python-dev \
      libboost-all-dev \
      libcurl4-openssl-dev \
      libsqlite3-dev \
      libdb5.3 \
      libmysqlclient-dev \
      libuv-dev libssl-dev \
      libarchive13 libarchive-dev \
      libatlas-base-dev libatlas-dev \
      unzip \
      nginx \
      ffmpeg \
      rsync \
      nodejs \
      cuda-core-8-0=$CUDA_PKG_VERSION \
      cuda-driver-dev-8-0=$CUDA_PKG_VERSION \
      cuda-nvrtc-dev-8-0=$CUDA_PKG_VERSION \
      cuda-nvgraph-dev-8-0=$CUDA_PKG_VERSION \
      cuda-cusolver-dev-8-0=$CUDA_PKG_VERSION \
      cuda-cublas-dev-8-0=$CUDA_PKG_VERSION2 \
      cuda-cufft-dev-8-0=$CUDA_PKG_VERSION \
      cuda-curand-dev-8-0=$CUDA_PKG_VERSION \
      cuda-cusparse-dev-8-0=$CUDA_PKG_VERSION \
      cuda-npp-dev-8-0=$CUDA_PKG_VERSION \
      cuda-cudart-dev-8-0=$CUDA_PKG_VERSION \
      openssh-server


## pip
RUN pip install --upgrade pip
RUN pip install --upgrade virtualenv
RUN pip install --upgrade virtualenv
RUN pip install -U setuptools
RUN pip install boto3 grpcio==1.4.0 requests numpy theano gensim
RUN pip install requests
 
##
RUN npm install -g @angular/cli@1.0.0

# account settings
# Create and configure minds user
RUN groupadd -g 1000 minds
RUN useradd -g 1000 -u 1000 -m -s /bin/bash minds
RUN mkdir /var/run/sshd
RUN echo 'root:screencast' | chpasswd
RUN echo 'minds:ggoggoma' | chpasswd
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

# sudo settings
RUN adduser minds sudo

## Enable passwordless sudo for users under the "sudo" group
RUN sed -i.bkp -e \
      's/%sudo\s\+ALL=(ALL\(:ALL\)\?)\s\+ALL/%sudo ALL=NOPASSWD:ALL/g' \
      /etc/sudoers

# Configure SSH access
RUN mkdir -p /home/minds/.ssh

# Enable universe
#RUN echo "deb http://archive.ubuntu.com/ubuntu xenial main universe" > /etc/apt/sources.list

# Cuda runtime setting
RUN ln -s cuda-8.0 /usr/local/cuda
RUN rm -rf /var/lib/apt/lists/*

RUN echo "/usr/local/cuda/lib64" >> /etc/ld.so.conf.d/cuda.conf && \
    ldconfig

RUN echo "/usr/local/nvidia/lib" >> /etc/ld.so.conf.d/nvidia.conf && \
    echo "/usr/local/nvidia/lib64" >> /etc/ld.so.conf.d/nvidia.conf

ENV PATH /usr/local/nvidia/bin:/usr/local/cuda/bin:${PATH}
ENV LD_LIBRARY_PATH /usr/local/nvidia/lib:/usr/local/nvidia/lib64

VOLUME [/home/minds/.minds-build]
VOLUME [/home/minds/minds]
VOLUME [/home/minds/git]

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
