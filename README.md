# Concordance

**Problem Statement**: Given an arbitrary text document written in English,
write a program that will generate a concordance, i.e. an alphabetical list
of all word occurrences, labeled with word frequencies. As a bonus: label
each word with the sentence numbers in which each word occurrence appeared.

See the problem statement in the original formatted pdf
[problem.pdf](problem.pdf). It includes sample formatted output which
implies additional problem requirements and behavior.

## Solutions

### Brute Force
For details about that design approach and solution,
see [brute/README.md](brute/README.md).

### MapReduce
For details about that design approach and solution,
see [mr/README.md](mr/README.md).

## Virtual Environment

Create a virtual environment.
```
> python -m venv concordance
> concordance\Scripts\activate
```

Install the project requirements.
```
(concordance) > cd <this_project>
(concordance) > pip install -r requirements.txt
```
