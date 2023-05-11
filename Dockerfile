FROM ubuntu:20.04

LABEL authors="Maja Franz <maja.franz@othr.de>, Tobias Winker <t.winker@uni-luebeck.de>"

ENV DEBIAN_FRONTEND noninteractive
ENV LANG="C.UTF-8"
ENV LC_ALL="C.UTF-8"

# Install required packages
RUN apt-get update && apt-get install -y \
        python3 \
        python3-pip


# Add user
RUN useradd -m -G sudo -s /bin/bash tutorial && echo "tutorial:tutorial" | chpasswd
RUN usermod -a -G staff tutorial
USER tutorial

# Add artifacts (from host) to home directory
ADD --chown=tutorial:tutorial . /home/tutorial/tutorial

WORKDIR /home/tutorial/tutorial

# install python packages
ENV PATH $PATH:/home/tutorial/.local/bin
RUN pip3 install -r requirements.txt

CMD ["./run.sh"]
