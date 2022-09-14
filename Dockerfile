FROM 812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base:6839-main

RUN apt-get install curl libtool-bin -y

RUN curl https://codeload.github.com/TimoLassmann/kalign/tar.gz/refs/tags/v3.3.2 --output kalign-3.3.2.tar.gz && tar -zxvf kalign-3.3.2.tar.gz

RUN cd kalign-3.3.2 && ./autogen.sh && ./configure && make && make check && make install

RUN python3 -m pip install --upgrade latch
COPY wf /root/wf
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
WORKDIR /root
