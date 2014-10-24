atypical
========

Find the junk data hidden amongst the good data (Python 3.4)

Automatically identifying and removing low quality data is important whenever
dealing with large quantities of organically generated information. Many fields
can have a reasonable level of quality enforced by simply using a regex, e.g.,
URLs, email addresses, phone numbers. However ensuring quality with data that
doesn't have a strict format or syntax can be much trickier. This library uses
a combination of the Markov property and character proportions to infer which
data points are the most out of place.

## Usage:
This example prints the strings ordered by how typical they are relative to the
other strings. `'ax'` is the least typical, while `'ab'` is the most typical.

```python
>>> from atypical import atypical
>>> scores = atypical(['abb', 'ax', 'ab', 'ab', 'abc'])
>>> list(scores.rounded())
[(-1.457, 'ax'), (-0.439, 'abc'), (0.146, 'abb'), (0.823, 'ab')]
>>> list(scores.objects())
['ax', 'abc', 'abb', 'ab']
>>> list(scores.standardized().rounded()) # z-scores
[(-1.268, 'ax'), (-0.215, 'abc'), (0.391, 'abb'), (1.092, 'ab')]
```

## Dependencies:
* Python 3.4
* [iterlib](https://github.com/rectangletangle/iterlib)
* requests *(only for the scripts)*
* Beautiful Soup *(only for the scripts)*

## Installation:
```bash
$ python3 setup.py install
```
