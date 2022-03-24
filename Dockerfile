FROM openmodelica/openmodelica:v1.18.0-ompython

RUN pip3 install Flask scipy
RUN pip3 install DyMat
COPY ./bin/setup_modelica.py /usr/bin/
RUN mkdir /app/
RUN mkdir /app/static/
RUN mkdir /app/templates/

RUN useradd -ms /bin/bash openmodelica
RUN chown openmodelica /usr/bin/omc
USER openmodelica
RUN chmod 4755 /usr/bin/omc
ENV USER openmodelica
RUN python3 /usr/bin/setup_modelica.py

WORKDIR /app
COPY ./main.py /app/
COPY ./static/template.css /app/static/
COPY ./templates/home.html /app/templates

ENTRYPOINT ["python3"]
CMD ["main.py"]

EXPOSE 80
