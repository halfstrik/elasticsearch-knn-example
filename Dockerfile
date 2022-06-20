FROM elasticsearch:7.17.4
RUN elasticsearch-plugin install --batch https://github.com/alexklibisz/elastiknn/releases/download/7.17.4.0/elastiknn-7.17.4.0.zip
