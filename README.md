<div align="center">
    <h1>Pop20c Corpus</h1>
    <p>A corpus of the top Billboard songs from 1900–1999</p>
</div>

The *Pop20c Corpus* includes 100 songs of American popular music: the most popular song from each year of the 20th century. The songs from 1900 through 1954 were selected based on the charts from Joel Whitburn's book *A Century of Pop Music*; these charts in turn were based on other charts reflecting record sales as well as other media such as sheet music sales, radio play, and jukebox play. Songs from 1955 through 1999 were selected from the *Billboard Hot 100* chart.

The *Pop20c Corpus* was developed by <a href="https://www.josephvanderstel.com/" target="_blank">Joseph VanderStel</a> (joe.vanderstel@gmail.com) and <a href="http://davidtemperley.com/" target="_blank">David Temperley</a> (dtemperley@esm.rochester.edu). For more about our methodology, see our article “The Evolution of Syncopation in Twentieth-Century American Popular Music” in *Journal of New Music Research* (2022). (<a href="https://www.josephvanderstel.com/pdfs/vanderstel_temperley_2022.pdf" target="_blank">PDF</a>) We originally developed the corpus in connection with that study, but it may also be useful for other music researchers and enthusiasts who wish to study the rich tradition of American popular music.

Songs are encoded as complete vocal melodies using a modified version of a format used in the <a href="http://rockcorpus.midside.com/index.html">*Rolling Stone Corpus*</a>. Encodings are based on transcriptions from recordings rather than sheet music.

There are three files associated with each song. Below is a summary of each file, using the opening measures of John McCormack's “It's A Long Way To Tipperary” (1915) as an example:

![John McCormack, "It's A Long Way To Tipperary" (1915)](https://github.com/vanderstel/pop-corpus/blob/master/static/imgs/tipperary.png?raw=true)

---

#### 1. The transcription file (<a href="https://github.com/vanderstel/pop-corpus/tree/master/transcriptions_raw">/transcriptions_raw</a>)

The scale degrees and rhythms of the melody are encoded using a format that enables rapid transcription of the song in near real time. Here are the opening measures of the transcription file for "It's A Long
Way To Tipperary":


```
1..3 2~1~ 6~5~ 3~45 | ~~6~ 5~3~ 5~~~ .... |
```


This is almost identical to the format that is used in the *Rolling Stone Corpus* (<a href="http://rockcorpus.midside.com/melodic_transcriptions.html">click here for an overview</a>), with one exception: in the *Rolling Stone Corpus*, both continuations and rests are encoded with periods (`.`), but the present corpus differentiates continuations with a tilde (`~`). 

___


#### 2. The lyric file (<a href="https://github.com/vanderstel/pop-corpus/tree/master/lyrics">/lyrics</a>)

The corpus includes lyrics for each song, which were crosschecked with multiple sources on the internet. Here are the lyrics of the above excerpt:

```
Up to mighty London came
An Irish man one day
```

---

#### 3. The "note list" file (<a href="https://github.com/vanderstel/pop-corpus/tree/master/transcriptions_notelist">/transcriptions_notelist</a>)

A "note list" file is generated from the transcription and lyric files using a custom script, and is designed to be machine-readable. The output file represents each melody as a list of note statements. Here is the note list for the above excerpt:

```
4.0000 4.0625 60 0 0 UP[1]
4.1875 4.2500 64 4 0 TO[1]
4.2500 4.3750 62 2 1 MIGHTY[1]
4.3750 4.5000 60 0 0 MIGHTY[2]
4.5000 4.6250 57 9 1 LONDON[1]
4.6250 4.7500 55 7 0 LONDON[2]
4.7500 4.8750 52 4 1 CAME[1]
4.8750 4.9375 53 5 0 AN[1]
4.9375 5.1250 55 7 1 IRISH[1]
5.1250 5.2500 57 9 0 IRISH[2]
5.2500 5.3750 55 7 1 MAN[1]
5.3750 5.5000 52 4 0 ONE[1]
5.5000 5.7500 55 7 1 DAY[1]

```

Each line contains six values:
- The first value is the time point of the note’s onset relative to the beginning of
the song. The measure is the basic unit, with decimals representing divisions of the measure. For example, `5.2500` means the second quarter-note beat of the fifth measure.
- The second value is the duration of the note. Again, the measure is the unit, with decimals representing fractions of the measure.
- The third value is the MIDI number of the note (following the usual convention of
middle C = 60).
- The fourth value is the note's chromatic scale degree integer (tonic=0; leading tone=11).
- The fifth value is the lexical stress of the syllable, with `1` being stressed, and `0`
being unstressed.
- The sixth value is the syllable itself. For example, `MIGHTY[2]` refers to
the second syllable of the word "mighty."

Syllabic stress values are calculated by mapping each syllable from the lyric file to one of three stress values according to the <a href="http://www.speech.cs.cmu.edu/cgi-bin/cmudict">Carnegie Mellon University Pronouncing Dictionary</a>: 0 for unstressed syllables
(*to*-ma-to), 1 for stressed syllables (to-*ma*-to), and 2 for syllables with secondary stress
(to-ma-*to*). Following the convention of <a href="http://rockcorpus.midside.com/lyrics_stress.html">prior studies</a>, all monosyllabic function words (such as articles, pronouns, and
prepositions) are assigned an unstressed syllable, and 2's are converted to 1's, i.e. treated as
stressed syllables.




