FROM logstash:5

RUN logstash-plugin install logstash-filter-de_dot

COPY logstash.conf /etc/logstash/conf.d/logstash.conf

CMD ["logstash", "-f", "/etc/logstash/conf.d/logstash.conf"]
#CMD ["-f", "/some/config-dir/logstash.conf"]
