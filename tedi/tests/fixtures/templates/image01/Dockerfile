FROM ubuntu

# Here's a little fixture to test whether Jinja template tags get expanded.
LABEL two_plus_two={{ 2 + 2 }}

# Here's one to test if our facts, from the Facts() class get expanded.
LABEL test_canary_fact="{{ test_canary_fact }}"

CMD ["echo", "text fixture"]
