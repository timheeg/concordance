# Concordance: MapReduce

This solution employs a MapReduce style approach.
However, I did not have access to the infrastructure necessary to set up
the Hadoop cluster on which to run this code via hadoop. 

**Restriction**:  My current development environment is controlled by my
current workplace. It restricts both permissions to docker hub and
permissions to run docker desktop on the laptop.

**Work around**: Therefore this solution is just a pseudo-MapReduce approach.
It was tested by emulating MapReduce processing linearly using pipes without
the parallelization of the hadoop cluster.

## MapReduce Approach

The `splitter` uses NLP to chop up the input data into English sentences.
Instead of farming out lines of input to mappers, the splitter reads multiple
lines and breaks them into sentences. It removes any `\n` newlines that may
remain in the sentence from the original input file. It outputs the sentence
index along with the sentence.

```
1   Hello, world.
2   Hello, world.
```

The `mapper` reads each line of input received and holds onto the sentence
index. It then uses NLP to tokenize the sentence into words. It then outputs
each word along with the sentence index it was found in.

```
Hello 1
World 1
Hello 2
World 2
```

The data is (shuffled) sorted before processed by the reducer. This aligns
common word entities together.

```
Hello 1
Hello 2
World 1
World 2
```

The `reducer` reads each line of input received and holds onto the word and
adds the sentence index to an empty list. If the next line parsed is for the
same word, then the new sentence index is appended to the existing list.
When the next line parsed is for a different word, the reduce writes out
data for the last word it was processing, including the word and the list
of all sentence indexes encountered.

```
Hello 1,2
World 1,2
```

The `output` function reads each line of input received and outputs the
final concordance format including the list item prefix, the word, the
word count (just the length of the sentence index list), and the sentence
index list.

```
a. Hello  {2:1,2}
b. World  {2:1,2}
```

## Problems

### Windows Sorting Failures

On Windows 10, where I'm running this solution, its `sort` is case insensitive
such that sorting the output of the `mapper` results in a mixture of case.

```
v.                       aliquam          {6:1300,1303,1307,1318,1323,1328}
w.                       Aliquam          {1:1329}
x.                       aliquam          {4:145,148,156,174}
y.                       Aliquam          {2:185,195}
z.                       aliquam          {8:219,23,234,250,254,269,277,300}
```

Since these words on not properly sorted, the `reducer` identifies different
case as different words, as expected; but this results in the `reducer`
treating each change of case as a different word in the concordance.

I googled this Windows sort problem and tried the solution of setting the
local to C for ascii sorting using `sort /L C` but this did not alter my
sorting output in anyway.

This is a catastrophic failure for processing and concordance generation.
Therefore, I implemented a `sorter` which sorts the `mapper` output lines
in order to solve this problem.

Running this through a true hadoop cluster would avoid this sort issue
and make the `sorter` unnecessary.


### Sentence Identification Bottleneck

The `splitter` for this solution efficiently splits input into sentences
by processing batches of lines of input at a time. This allows the NLP
to process large text inputs in small chunks.

However, the problem with this approach is that the `splitter` is still
a single linear batching process. So the `splitter`, while far more efficient
than NLP processing the entire text in memory, is a performance bottleneck.

The `splitter` and sentence identification needs to be parallelized with a
slightly different approach in order to reduce processing time.

### Concordance Item Prefix and Item Spacing

Since the concordance item prefix in this solution requires knowledge
of the total number of words in order to provide justification spacing
of the prefixes in the final output, then this inherently requires
processing of all `reducer` output before the answer can be determined.

Similarly, since the concordance word entry in the this solution requires
knowledge of the length of the longest word in order to provide justification
spacing of the entries in the final output, then this similarly requires
processing of all `reducer` output before the answer can be determined.

The `outputer` in this solution saves off all concordance data in memory
while determining the longest word and total words, before writing the
final output which is both time and memory inefficient.

This could be slightly improved by having the `reducers` calculate the
word length and word count themselves and then output this metadata as
the final line of output. The `outputer` could process these values and
then determine the max values received from all `reducers`. This may reduce
the time the `outputer` spends trying to calculate these values from the
entire concordance dataset, however the result is still both time and
memory inefficient.


## Running

Active the virtual environment.
```
> source <env>/concordance/Scripts/activate
```

Grant execution permissions to the python source files.
```
(concordance) > chmod +x splitter.py mapper.py
    sorter.py reducer.py outputer.py
```

Emulate the MapReduce execution by piping the commands together.
```
(concordance) > cat ../res/example.txt | ./splitter.py
    | ./mapper.py | ./sorter.py
    | ./reducer.py | ./outputer.py
```

Save the output.
```
(concordance) > cat ../res/example.txt | ./splitter.py
    | ./mapper.py | ./sorter.py
    | ./reducer.py | ./outputer.py >
    output/example.concordance.txt
```

## Examples

The ```/res``` folder contains a couple examples.

* ```example.txt``` is the text provided in the problem statement.
* ```20k.txt``` is approx. 20k words of random "Lorem ipsum" text.
* ```turing.txt``` is a rudimentary copy of Alan Turing's "Turing Test" paper.

The ```/output``` folder contains the results of the concordance
(pseudo) mapreduce solution run against those example inputs.


## References

Wright State CSE 7380 Cloud Computing personal course notes from 2016.
