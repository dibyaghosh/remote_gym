FROM continuumio/miniconda
RUN conda create -n env python=3.8
RUN echo "source activate env" > ~/.bashrc
ENV PATH /opt/conda/envs/env/bin:$PATH
RUN echo $(which python)
RUN pip install gym==0.23.1
RUN pip install git+https://github.com/dibyaghosh/docker_gym.git
CMD [""]