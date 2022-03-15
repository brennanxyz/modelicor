FROM python:3.7
ENV GIT_SSL_NO_VERIFY 1

COPY ./bin/modelica_*.sh /build/
RUN chmod +x /build/modelica_*.sh

RUN /build/modelica_prepare.sh
RUN /build/modelica_install.sh

COPY ./requirements.txt /app/
WORKDIR /app
RUN mkdir /app/templates
COPY ./templates/* /app/templates/
RUN pip3 install -r requirements.txt
COPY ./main.py /app/
RUN chmod -R 776 main.py
RUN useradd -ms /bin/bash openmodelica
USER openmodelica
ENV USER openmodelica
ENTRYPOINT ["python"]
CMD ["main.py"]

EXPOSE 80
