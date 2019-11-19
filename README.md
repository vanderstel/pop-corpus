<div align="center">
<h1>Pop Corpus</h1>
<p>A corpus of the top Billboard songs from 1900–1999</p>
</div>

<h2>Setup</h2>
<section>
  <h3>Tools</h3>
  <p></p>
  <ul>
    <li>MAMP - for MySQL database</li>
    <li>Postman - for API testing</li>
  </ul>
</section>
<section>
  <h3>Installation</h3>
  <p>Once a Virtual environment has been initialized, `cd` into the project directory. Do the following:</p>

  ```
  export FLASK_APP=app.py
  pip install -r requirements.txt
  pip install --editable .
  euphony db reset
  ```

  <p>Next, open up MAMP and fire up the local database engine. This should be running on localhost:8889. You will have to add a database named "euphony". (See settings.py for database config.)</p>

  <p>To run the flask app: `python run.py`</p>
</section>

<h2>Current limitations of the editor</h2>
<p>See `LIMITATIONS` under `app/utils/constants`.</p>
<section>
  <ul>
    <li>ADD_MEASURE only adds a measure to the end of the exercise (not in the middle).</li>
    <li>The number of beats in an exercise cannot exceed 16. (LIMITATIONS.maxBeats)</li>
    <li>There can only be one system: SVGVARS.maxBeatsPerSystem == LIMITATIONS.maxBeats.</li>
    <li>ADD_KEY and ADD_METER only set the key and meter at the beginning, meaning that an exercise currently can only have one key or meter.</li>
    <li>CHANGE_EVENT_DURATION can only augment to a half note, or diminute to an 8th note.</li>
  </ul>
</section>
